#coding=utf-8
import pymssql

class DaoSupport():
    def __init__(self, host, user, passwd, db=''):
        self.conn=pymssql.connect(host=host, user=user, password=passwd, database=db, charset='utf8')
        self.cur=self.conn.cursor()
        
    def close(self):
        self.cur.close()
        self.conn.close()

    def execOther(self, sql, params=None):
        if params is None:
            self.cur.execute(sql)
        else:
            s=sql % params
            print s
            self.cur.execute(s)
            

    def execQuery(self, sql, params=None):
        if params is None:
            self.cur.execute(sql)
            return self.cur.fetchall()
        s=sql % params
        self.cur.execute(s)
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()





