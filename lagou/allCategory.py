#### 本方法用于获取所有职位分类页面
## 入口url https://www.lagou.com/

import requests
from dbHandle import dbHandle
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}


#获取所有职位分类url 入库
def allCategory(url):

    s = requests.session()
    s.headers.update(headers)
    db = dbHandle()
    r = s.get(url)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        text = r.text
        obj = etree.HTML(text)


    #职位分类
    jobCategory = r'//*[@id="sidebar"]/div//div'

    #职位细分-分类
    detailCategory = r'./div[2]//dl/dd//a'

    #职位名
    jobTitle = r'./text()'

    #职位ur
    jobUrl = r'./@href'

    allCategorys = obj.xpath(jobCategory)

    for catetory in allCategorys:
        if len(catetory.xpath(detailCategory))!=0:
            for job in catetory.xpath(detailCategory):
                # print(job.xpath(jobTitle)[0])
                # print(job.xpath(jobUrl)[0])
                sql = """insert into jobCategories(category_name,category_url) values('{0}','{1}')""".\
                    format(job.xpath(jobTitle)[0],job.xpath(jobUrl)[0])
                db.insert_db(sql)

allCategory('https://www.lagou.com/')