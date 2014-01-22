# -*- coding: utf-8 -*-
import pypyodbc, time

conn = pypyodbc.connect("DRIVER={SQL Server};SERVER=192.168.2.5;UID=sde;PWD=sde;DATABASE=HZ_BUS")
cur = conn.cursor();

#创建alphaTable2
cur.execute(u'''
IF EXISTS (
    SELECT  TABLE_NAME FROM HZ_BUS.INFORMATION_SCHEMA.TABLES
    WHERE   TABLE_NAME = 'alphaTable2')
DROP TABLE  HZ_BUS.dbo.alphaTable2;

select * into alphaTable2
from 
(
select lineid,linedir,stopInfo,AVG(internalTime) as averageInternalTime,
internalIndex,timeIndex,dayType,quarter,100.00/100 as cfftOfVar
from alphaTable1
group by lineid,linedir,stopInfo,internalIndex,timeIndex,dayType,quarter
)
as t;

alter table HZ_BUS.dbo.alphaTable2
alter column cfftOfVar numeric(30,20);
''')
conn.commit()

#计算alphaTable1中的平均值并更新alphaTable2中的averageInternalTime
# 先获取所有的groups
cur.execute(u'''select distinct lineid, linedir, internalIndex,timeIndex,dayType, quarter from alphaTable1''')
groups = cur.fetchall()
tg = len(groups)
print 'total groups:', tg

#抓取所有的数据 5天的是400M内存
sql = '''SELECT [lineid],[linedir],[tid],[runIndex],[fromStopIndex],[toStopIndex],[stopInfo],
      [internalTime],[internalIndex],[timeIndex],[dayValue],[dayType],[quarter]
      FROM [HZ_BUS].[dbo].[alphaTable1]'''
cur.execute(sql)
resList = cur.fetchall()
print 'number of total items', len(resList)

'''
lineid,           0
linedir,          1
internalIndex,    2
timeIndex,        3
dayType,          4
quarter           5
'''

#ssToExe = []
#logFile = open('d:/sql.txt','a')
InvalidN = 0
begin = time.time()
updateSQL = u'''update [HZ_BUS].[dbo].[alphaTable2] set averageInternalTime = %d
              where lineid=%d and linedir=%d and internalIndex=%d and
              timeIndex=%d and dayType=%d and quarter=%d'''
for i,g in enumerate(groups):
      t=sorted([elem for elem in resList \
            if elem[0]==g[0] and elem[1]==g[1] and elem[8]==g[2] and elem[9]==g[3] and \
               elem[11]==g[4] and elem[12]==g[5]],key=lambda e:e[7])
      itemsN = len(t)
      if itemsN<10:
            InvalidN = InvalidN + 1
      t=t[int(round(itemsN*0.03)):int(round(itemsN*0.97))]   #去掉前 3% 和后 3% 的极端数据
      gl=list(g)
      gl.insert(0,sum([e[7] for e in t])/len(t))
      updateSQLR = updateSQL % tuple(gl)
      #ssToExe.append(updateSQLR)
      if i%30 is 0:
            print 'schedule---', (i*1.0000/tg)
      cur.execute(updateSQLR)
      conn.commit()

'''
for s in ssToExe:
      logFile.write(s)
      logFile.write(';\r\n')
logFile.close()'''

print u'Invalid number is', InvalidN


#计算变化系数
cur.execute('''
update [HZ_BUS].[dbo].[alphaTable2] 
set cfftOfVar = t2.factor
from HZ_BUS.dbo.alphaTable2 as t1,
(
select b.lineid,b.linedir,b.stopInfo,b.internalIndex,
b.timeIndex,b.dayType,b.quarter,b.averageInternalTime*1.00/a.averageInternalTime as factor
from HZ_BUS.dbo.alphaTable2 a,HZ_BUS.dbo.alphaTable2 b
where a.lineid = b.lineid and 
      a.linedir = b.linedir and 
      a.stopInfo = b.stopInfo and 
      a.internalIndex = b.internalIndex and 
      a.timeIndex = b.timeIndex-1 and 
      a.dayType = b.dayType and 
      a.quarter = b.quarter
) as t2
where t1.lineid = t2.lineid and 
      t1.linedir = t2.linedir and 
      t1.stopInfo = t2.stopInfo and 
      t1.internalIndex = t2.internalIndex and 
      t1.timeIndex = t2.timeIndex and 
      t1.dayType = t2.dayType and 
      t1.quarter = t2.quarter
''')
conn.commit()
conn.close()

print 'total run time is', (time.time()-begin)


