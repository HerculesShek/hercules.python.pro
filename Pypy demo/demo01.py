# -*- coding: utf-8 -*-
import pymysql
 
try:
    conn=pymysql.connect(host='localhost',user='root',passwd='xrt512',db='pythonDemo',port=3306)
    cur=conn.cursor()
    cur.execute('select * from scores')
    f = cur.fetchone()
    print f
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
