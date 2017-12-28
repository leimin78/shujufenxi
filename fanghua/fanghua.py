### 电影芳华--豆瓣短评抓取
### 入口url https://api.douban.com/v2/movie/subject/26862829/reviews?apikey=0b2bdeda43b5688921839c8ecb20399b&start=0&count=20&client=something&udid=""

import requests
import json
from dbHandle import dbHandle

fanghua_url = "https://api.douban.com/v2/movie/subject/5350027/reviews?apikey=0b2bdeda43b5688921839c8ecb20399b&start={0}&count=100&client=something&udid="

class fanghua:
    def __init__(self):
        self.s = requests.session()
        self.db = dbHandle()

    #获取总评论数
    def getTotal(self):
        text = self.s.get(fanghua_url.format('0')).text
        text_dict = json.loads(text)
        total = (text_dict['total'])
        return total

    #将短评数据插入数据库
    def comment_db(self):
        total = self.getTotal()
        start = 0

        #循环获取数据
        while start < total:
            text_dicts = json.loads(self.s.get(fanghua_url.format(str(start))).text)
            for text_dict in text_dicts['reviews']:
                #用户名
                user_name = text_dict['author']['name']

                #电影评分
                film_star = text_dict['rating']['value']

                #电影评论时间
                film_comment_time = text_dict['created_at']

                #评论点赞数
                comment_agree = text_dict['useless_count']

                #评论内容
                comment_content = text_dict['content']

                print("用户名:{0}".format(user_name))
                print("电影评分:{0}".format(film_star))
                print("电影评论时间:{0}".format(film_comment_time))
                print("评论点赞数:{0}".format(comment_agree))
                print("评论内容:{0}".format(comment_content))

                insert_sql = "insert into maoyao(user_name,film_star,film_comment_time,comment_agree,comment_content) values('{0}','{1}','{2}','{3}','{4}')".format(user_name,film_star,film_comment_time,comment_agree,comment_content)
                self.db.insert_db(insert_sql)
            start += 100


if __name__ == '__main__':
    fanghua1 = fanghua()
    fanghua1.comment_db()
