# -*- coding: utf-8 -*-
# @Time    : 17/12/12 下午3:13
# @Author  : LM
# 获取公司信息,职位信息

import requests
import json
import time
from random import randint
from dbHandle import dbHandle

# 定义消息头
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '40',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'user_trace_token=20171211135822-4b4007c1-de38-11e7-9cc5-5254005c3644; LGUID=20171211135822-4b400a8e-de38-11e7-9cc5-5254005c3644; index_location_city=%E6%B7%B1%E5%9C%B3; X_HTTP_TOKEN=5de0c472526daa35af4532ca48e2df84; JSESSIONID=ABAAABAAADEAAFI2622590B33836FA6C4A644F84644FC28; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_navigation; _gid=GA1.2.898922397.1512971907; _ga=GA1.2.721015615.1512971906; LGSID=20171213174246-f9827066-dfe9-11e7-9d0d-5254005c3644; LGRID=20171213175512-b5e6f8e4-dfeb-11e7-9463-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512971907; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1513158913; SEARCH_ID=ae724cdc7dfe4ac6aa4a8db5dfb47902',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_BD%E7%BB%8F%E7%90%86?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest'
}

query_sql = 'select category_name from jobCategories'
query_companyid_sql = 'select companyId from company_detail where companyID={0}'
query_position_sql = 'select positionId from position_detail where positionId={0}'


class lagouCompany:
    # 初始化
    def __init__(self):

        # 初始化session,数据链接
        self.db = dbHandle()
        self.s = requests.session()
        self.s.headers.update(headers)
        self.post_url = """https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false&isSchoolJob=0"""
        #self.post_url = """https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false&isSchoolJob=0"""

    # 买的代理2分钟更新一次每次3个IP
    def get_proxy(self):
        r = requests.get("http://proxy.httpdaili.com/api.asp?ddbh=aass&sl=20&noinfo=true&text=true")
        # ip_ports = json.loads(r.text)
        # maxint = len(ip_ports) - 1
        # index = randint(0, maxint)
        # ip_port = [ip_ports[index][0], ip_ports[index][1]]

        IPlist=r.text.split('\r\n')[:20]
        return IPlist

    # 获取分类的页数
    def get_category_page(self, category):
        postdata = {
            'first': 'false',
            'pn': 1,
            'kd': category[0]
        }
        retry_cout = 10
        while retry_cout > 0:
            try:
                proxy = self.get_proxy()
                print("proxy:{0}".format(proxy))
                i = randint(0,19)
                page_text = self.s.post(self.post_url, data=postdata,
                                        proxies={"https": "https://{0}".format(proxy[i])}, timeout=30)
                page_dict = json.loads(page_text.text)
                total_count = page_dict['content']['positionResult']['totalCount']
                print("total_count:{0}".format(total_count))
                #total_page = page_dict['content']['pageSize']
                total_page = int(total_count / 15) + 1
                print("获取分类:{1},总页数:{0}将暂停10s".format(total_page,category[0]))
                return total_page
            except Exception as e:
                print(e.args)
                retry_cout -= 1
                time.sleep(2)

    # 获取公司信息
    def get_company(self, page, category):
        postdata = {
            'first': 'false',
            'pn': page,
            'kd': category
        }

        retry_count = 9
        while retry_count > 0:
            try:
                proxy = self.get_proxy()
                print("proxy:{0}".format(proxy))
                i = randint(0,19)
                time.sleep(2)
                page_text = self.s.post(self.post_url, postdata,
                                        proxies={"https": "https://{0}".format(proxy[i])}, timeout=30)
                page_dict = json.loads(page_text.text)
                print(page_dict)

                company_result = page_dict['content']['positionResult']['result']
                print(company_result)
                print(company_result[0].keys())
                return company_result
            except Exception as e:
                print(e.args)
                if(e.args[0] == 'list index out of range'):
                    break
                retry_count -= 1
                time.sleep(2)

    # 获取分类数据
    def get_category(self):
        self.db.query_db(query_sql)
        datas = self.db.datas
        return datas


if __name__ == '__main__':
    lagou_company = lagouCompany()

    # 获取所有分类
    categories = lagou_company.get_category()

    # 获取各分类下所有公司信息
    for category in categories[199:]:

        # 获取接口页数

        total_page = lagou_company.get_category_page(category)
        print("{0}分类共{1}页".format(category[0],total_page+1))
        # 获取所有公司信息
        for page in range(1, total_page + 1):
            print("正在获取分类:{0},第{1}页数据".format(category[0],page))
            company_result = lagou_company.get_company(page, category[0])
            # print(company_result['companyId'])
            # print(company_result['city'])
            # print(company_result['district'])
            # print(company_result['financeStage'])
            # print(company_result['industryField'])
            # print(company_result['companySize'])
            # print(company_result['companyLabelList'])
            # print(company_result['companyFullName'])
            try:
                for result in company_result:

                    #公司数据
                    companyId = result['companyId']
                    city = result['city']
                    district = result['district']
                    financeStage = result['financeStage']
                    industryField = result['industryField']
                    companySize = result['companySize']
                    companyLabelList = result['companyLabelList']
                    companyFullName = result['companyFullName']

                    #拼装公司sql数据
                    company_sql = """insert into company_detail(companyId,city,district,financeStage,industryField,companySize,companyLabelList,companyFullName) \
                    values('{0}','{1}','{2}','{3}','{4}','{5}',"{6}",'{7}')""".format(companyId,city,district,financeStage,industryField,companySize,companyLabelList,companyFullName)

                    print("company_sql:{0}".format(company_sql))

                    #公司数据入库
                    db = dbHandle()
                    company_datas = db.query_db(query_companyid_sql.format(companyId))

                    #如果公司id不存在则入库
                    if len(company_datas) == 0:
                        db.insert_db(company_sql)


                    #职位数据
                    position_id = result['positionId']
                    position_name = result['positionName']
                    position_workYear = result['workYear']
                    position_education = result['education']
                    position_companyId = result['companyId']
                    position_salary = result['salary']
                    position_Advantage = result['positionAdvantage']
                    position_createTime = result['createTime']
                    position_Lables = result['positionLables']
                    position_category = category[0]

                    #拼装职位sql
                    position_sql = """ insert into position_detail\
                    (positionId,positionName,workYear,education,companyId,salary,\
                    positionAdvantage,createTime,positionLables,category) values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}")""".format(position_id,position_name,position_workYear,position_education,position_companyId,position_salary,position_Advantage,position_createTime,position_Lables,position_category)

                    print("position_sql:{0}".format(position_sql))
                    #职位数据入库

                    position_datas = db.query_db(query_position_sql.format(position_id))

                    #如果职位数据不存在则入库
                    if len(position_datas) == 0:
                        db.insert_db(position_sql)
            except Exception as e:
                print(e.args)