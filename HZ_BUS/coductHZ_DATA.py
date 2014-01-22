# -*- coding: utf8 -*-
import MySQLdb

def cat(lal,mam):
      v = list(map(lambda x: x[0]+" "+x[1], zip(lal.split(","), mam.split(","))))
      return ",".join(v)
try:
      conn=MySQLdb.connect(host='192.168.2.31',user='root',passwd='1234',db='shapefiles',port=3307)
      cur=conn.cursor()
      d = {}
      cur.execute('''SELECT linkID,AsText(GeomFromWKB(shapeInfo)) FROM shapefiles.hz_link_bus where linkID in
      (SELECT linkID FROM shapefiles.hz_mi);''')
      res1=cur.fetchall()
      for t in res1:
            d[t[0]]=t[1].split("(")[1].split(")")[0]
      cur.execute('''SELECT linkID,AsText(GeomFromWKB(shapeInfo)) FROM shapefiles.hz_mi where linkID in (
                  SELECT linkID FROM shapefiles.hz_link_bus);''')
      res2=cur.fetchall()
      for tt in res2:
            sql = '''update shapefiles.hz_link_bus set shapeInfo2 = ' '''+ cat(d[tt[0]],tt[1].split("(")[1].split(")")[0]) +''' ' where linkID = '''+str(tt[0])
            #print sql
            cur.execute(sql)
            
      conn.commit()
      conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

'''ALTER TABLE `shapefiles`.`hz_link_bus` ADD COLUMN `shapeInfo2` MEDIUMTEXT NULL  AFTER `shapeInfo` ;'''


      
      
