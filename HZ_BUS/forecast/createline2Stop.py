#-*- coding: utf-8 -*-
import MySQLdb

conn=MySQLdb.connect(host='localhost',user='root',passwd='xrt512')
cur=conn.cursor()
conditionSQL='''SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'hz_bus'
AND table_name = 'line2Stop';
'''
cur.execute(conditionSQL)
res=cur.fetchone()
if res is None:
    sql=''' CREATE  TABLE `hz_bus`.`line2Stop` (
        `lineIdBus` INT NULL ,
        `stopIndex` INT NULL ,
        `lineDirect` INT NULL ,
        `stopID` INT NULL ,
        `stopName` VARCHAR(50) NULL ) ENGINE = MyISAM; '''
    cur.execute(sql)
else:
    sql = 'truncate hz_bus.basicstop'
    cur.execute(sql)
