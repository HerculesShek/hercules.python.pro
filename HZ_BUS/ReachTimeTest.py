# -*- coding: utf-8 -*-
import pymssql

conn=pymssql.connect(host="192.168.2.5",user="sde",password="sde",database="HZ_BUS",charset="utf8")
conn.autocommit(True)
cur = conn.cursor();

lastsSQL = '''SELECT TOP 1000
        [lineid]
      ,[linedir]
      ,[tid]
      ,[runIndex]
      ,[stopIndex]
      ,[time]
  FROM [HZ_BUS].[dbo].[FcdB_BasicDataStopX]
  order by time desc'''

cur.execute(lastsSQL)
lasts = cur.fetchall()

lastsToTestSQL = '''SELECT TOP 1000
       [lineid]
      ,[linedir]
      ,[tid]
      ,[runIndex]
      ,[stopIndex]
      ,[time]
  FROM [HZ_BUS].[dbo].[FcdB_BasicDataStop]
  where time > '2013-11-8 7:40:00' and 
	tid = %d and runIndex = %d'''
for last in lasts:
    lastsToTestSQLRes = lastsToTestSQL % (last[2], last[3])
    cur.execute(lastsToTestSQLRes)
    lastsToTest = cur.fetchall()
    lastBusSQL = '''SELECT stopIndex,time
                    FROM [HZ_BUS].[dbo].[FcdB_BasicDataStopX]
                    where lineid = {0} and linedir = {1} and tid = (
                      SELECT top 1 tid
                      FROM [HZ_BUS].[dbo].[FcdB_BasicDataStopX]
                      where lineid = {0} and linedir = {1} and  stopIndex = {2}
                      order by time desc
                    )and runIndex = (
                      SELECT top 1 runIndex
                      FROM [HZ_BUS].[dbo].[FcdB_BasicDataStopX]
                      where lineid = {0} and linedir = {1} and  stopIndex = {2}
                      order by time desc
                    ) and stopIndex between {3} and {2}
                    order by stopIndex;'''
    for lastsTo in lastsToTest:
        lastBusSQLRes = lastBusSQL.format(last[0], last[1], lastsTo[4], last[4])
        cur.execute(lastBusSQLRes)
        
        lastBus = cur.fetchall()
        if len(lastBus) == (lastsTo[4] - last[4] + 1):
            print lastBusSQLRes
            print last, len(lastBus)
    
    


