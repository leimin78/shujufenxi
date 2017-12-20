###数据库操作封装

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
        try:
            self.cur.execute(query)
            self.datas = self.cur.fetchall()
            return self.datas
        except Exception as e:
            print(e.args)

    def delete_db(self,delsql):
        try:
            self.cur.execute(delsql)
            self.conn.commit()
        except Exception as e:
            print(e.args)

    def update_db(self,updatesql):
        try:
            self.cur.execute(updatesql)
            self.conn.commit()
        except Exception as e:
            print(e.args)

    def insert_db(self,insertsql):
        try:
            self.cur.execute(insertsql)
            self.conn.commit()
        except Exception as e:
            print(e.args)

    def __del__(self):
        self.conn.close()