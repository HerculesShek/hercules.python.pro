#-*- coding: utf-8 -*-
import MySQLdb

conn=MySQLdb.connect(host='localhost',user='root',passwd='xrt512')
cur=conn.cursor()
conditionSQL='''SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'hz_bus'
AND table_name = 'basicstop';
'''
cur.execute(conditionSQL)
res=cur.fetchone()
if res is None:
    sql=''' CREATE  TABLE `hz_bus`.`basicStop` (
  `lineid` SMALLINT NULL ,
  `linedir` TINYINT NULL ,
  `tid` BIGINT NULL ,
  `runIndex` TINYINT NULL ,
  `stopIndex` TINYINT NULL ,
  `time` DATETIME NULL ) ENGINE = MyISAM; '''
    cur.execute(sql)
else:
    sql = 'truncate hz_bus.basicstop'
    cur.execute(sql)


    







