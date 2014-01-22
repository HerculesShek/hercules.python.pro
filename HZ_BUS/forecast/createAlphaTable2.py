# -*- coding: utf-8 -*-
import MySQLdb, time

conn=MySQLdb.connect(host="localhost",user="root",passwd="xrt512",db="hz_bus", port=3306)
cur = conn.cursor();

#创建alphaTable2

cur.execute(u'''
create table alphaTable2 as
select *
from 
(
select lineid,linedir,stopInfo,AVG(internalTime) as averageInternalTime,internalIndex,timeIndex,dayType,quarter,100.00/100 as cfftOfVar
from alphaTable1
group by lineid,linedir,stopInfo,internalIndex,timeIndex,dayType,quarter
) as t''')
conn.commit()

time.sleep(2)

#计算alphaTable1中的平均值并更新alphaTable2中的averageInternalTime 这个阶段的主要工作是过滤
cur.execute(u'''select distinct lineid, linedir, internalIndex,timeIndex,dayType, quarter from alphaTable1''')
groups = cur.fetchall()
groups = list(groups)

sql = '''SELECT lineid,linedir,tid,runIndex,fromStop,toStop,stopInfo,internalTime,internalIndex
      ,timeIndex,dayValue,dayType,quarter FROM hz_bus.alphaTable1'''
cur.execute(sql)
resList = cur.fetchall()
resList = list(resList)

'''
lineid,           0
linedir,          1
internalIndex,    2
timeIndex,        3
dayType,          4
quarter           5
'''

for g in groups:
      t=sorted([resList.pop(resList.index(elem)) for elem in resList \
            if elem[0]==g[0] and elem[1]==g[1] and elem[8]==g[2] and elem[9]==g[3] and \
               elem[11]==g[4] and elem[12]==g[5]],key=lambda e:e[7])
      t=t[int(round(len(t)*0.03)):int(round(len(t)*0.97))]   #去掉前 3% 和后 3% 的极端数据
      g=list(g)
      g.insert(0,sum([e[7] for e in t])/len(t))
      params=tuple(g)
      sql=u'''update hz_bus.alphaTable2 set averageInternalTime = %d
              where lineid=%d and linedir=%d and internalIndex=%d and
              timeIndex=%d and dayType=%d and quarter=%d''' % params
      cur.execute(sql)
      conn.commit()
      
#计算变化系数
cur.execute(u'''
UPDATE hz_bus.alphaTable2 AS t1,
	    (
	    SELECT b.lineid,b.linedir,b.stopInfo,b.internalIndex,
		  b.timeIndex,b.dayType,b.quarter,b.averageInternalTime*1.00/a.averageInternalTime AS factor
	    FROM hz_bus.alphaTable2 a,hz_bus.alphaTable2 b
	    WHERE a.lineid = b.lineid AND 
	    a.linedir = b.linedir AND 
	    a.stopInfo = b.stopInfo AND 
	    a.internalIndex = b.internalIndex AND 
	    a.timeIndex = b.timeIndex-1 AND 
	    a.dayType = b.dayType AND 
	    a.quarter = b.quarter
	    ) AS t2
SET t1.cfftOfVar = t2.factor
WHERE     t1.lineid = t2.lineid AND 
	  t1.linedir = t2.linedir AND 
	  t1.stopInfo = t2.stopInfo AND 
	  t1.internalIndex = t2.internalIndex AND 
	  t1.timeIndex = t2.timeIndex AND 
	  t1.dayType = t2.dayType AND 
	  t1.quarter = t2.quarter

''')
conn.commit()
conn.close()


