###数据库操作

import pymysql
import datetime


class dbHandle:
    # 初始化查询连接
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.conn = pymysql.connect('localhost', 'root', '123456', 'lagou',charset='utf8')
        self.cur = self.conn.cursor()

    def query_db(self, query):
        #执行语句,获取数据
        print(query)
        self.cur.execute(query)
        self.datas = self.cur.fetchall()
        return self.datas

    def delete_db(self,delsql):
        self.cur.execute(delsql)
        self.conn.commit()

    def insert_db(self,insertsql):
        self.cur.execute(insertsql)
        self.conn.commit()

    def __del__(self):
        self.conn.close()