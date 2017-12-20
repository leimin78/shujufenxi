## 获取职位的要求
import requests
from random import randint
from lxml import etree
from dbHandle import dbHandle
from multiprocessing import Pool
import time

Agent = [
    {"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
    {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
    {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
]

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'JSESSIONID=ABAAABAAAIAACBI00DC067F2838414B5729F33F19EE2431; user_trace_token=20171214154305-6b7a3d87-e0a2-11e7-9d35-5254005c3644; LGUID=20171214154305-6b7a4104-e0a2-11e7-9d35-5254005c3644; _gat=1; X_HTTP_TOKEN=4bcda354b2c4e737c68459bb2ae645ef; ab_test_random_num=0; _putrc=1728BBFBEC7C4F42; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B71066; hasDeliver=0; TG-TRACK-CODE=index_navigation; SEARCH_ID=94dd19f99be2400198893e2a661a95fe; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.882065693.1513237385; _ga=GA1.2.110267066.1513237385; LGSID=20171214170534-f1bf14ad-e0ad-11e7-9780-525400f775ce; LGRID=20171214173553-2de4b78c-e0b2-11e7-9d3e-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1513237385; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1513244154',
'Host':'www.lagou.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':Agent[randint(0, 4)]['User-Agent']
}

#获取职位描述为空的id进行数据提取
query_jobid_sql = 'select positionId from position_detail where positionText is NULL'

#查职位id对应的描述是否为空
job_detail_sql = 'select positionText from position_detail where positionId={0}'

class jobDetail:

    def get_proxy(self):
        r = requests.get("http://proxy.httpdaili.com/api.asp?ddbh=aass&sl=20&noinfo=true&text=true")
        IPlist=r.text.split('\r\n')[:20]
        print("IPlist:{0}".format(IPlist))
        return IPlist

    def get_job_detail(self,jobid):
        job_url = "https://www.lagou.com/jobs/{0}.html".format(jobid)
        retry_times = 10
        while retry_times >0:
            try:
                i = randint(0,19)
                proxy = self.get_proxy()
                s = requests.session()
                s.headers.update(headers)
                r = s.get(job_url,proxies={"https": "https://{0}".format(proxy[i])},timeout=30)
                #print(r.text)
                obj = etree.HTML(r.text)
                job_texts = obj.xpath('//*[@id="job_detail"]/dd[2]/div//p/text()')
                print("job_texts{0}".format(job_texts))
                if job_texts:
                    return job_texts
                else:
                    print("页面:{1},获取有问题重试第{0}次".format(retry_times,job_url))
                    job_texts = obj.xpath('//*[@id="job_detail"]/dd[2]/div//p//span/text()')
                    return job_texts
                    time.sleep(1)

            except Exception as e:
                retry_times -= 1
                print(e.args)

    def insert_data(self,data):
        #db = dbHandle()
        data = data
        db = dbHandle()
        print(data)
        texts = self.get_job_detail(data)
        text = '\n'.join(texts)
        text = text.replace('"',"'")

        # 如果职位id对应的描述为空则插入数据
        job_detail = db.query_db(job_detail_sql.format(data))
        print(job_detail)
        if job_detail[0][0] == None:
                update_sql = """update position_detail set positionText="{0}" where positionId='{1}'""".format(text,data)
                print("正在执行更新语句:{0}".format(update_sql))
                db.update_db(update_sql.format(text, data))

if __name__ == '__main__':

    lagou = jobDetail()
    while True:
        p = Pool(processes=10)
        for i in range(10):
            db = dbHandle()
            data = db.query_db(query_jobid_sql)[i][0]
            p.apply_async(lagou.insert_data,args=(data,))
        p.close()
        p.join()
    # db = dbHandle()
    # datas = db.query_db(query_jobid_sql)
    # lagou_job = jobDetail()
    # for data in datas:
    #     #爬去
    #     texts = lagou_job.get_job_detail(data[0])
    #     text = '\n'.join(texts)
    #
    #     #如果职位id对应的描述为空则插入数据
    #     job_detail = db.query_db(job_detail_sql.format(data[0]))
    #     print("jobdetail:{0}".format(job_detail[0][0]))
    #     if job_detail[0][0] == None:
    #         update_sql = "update position_detail set positionText='{0}' where positionId='{1}'".format(text,data[0])
    #         print("正在执行更新语句:{0}".format(update_sql))
    #         db.update_db(update_sql.format(text,data[0]))

    print("数据更新完成")

