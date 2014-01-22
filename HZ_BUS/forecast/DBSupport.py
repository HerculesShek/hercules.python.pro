import MySQLdb

class DaoSupport():
    def __init__(self, host, user, passwd, port=3306, db=''):
        self.conn=MySQLdb.connect(host=host, user=user, passwd=passwd, port=port, db=db)
        self.conn.set_character_set('utf8')
        self.cur=self.conn.cursor()
        
    def close(self):
        self.cur.close()
        self.conn.close()

    def execOther(self, sql, params=None):
        if params is None:
            self.cur.execute(sql)
        else:
            s=sql % params
            self.cur.execute(s)

    def execQuery(self, sql, params=None):
        if params is None:
            self.cur.execute(sql)
            return self.cur.fetchall()
        s=sql % params
        self.cur.execute(s)
        return list(self.cur.fetchall())





