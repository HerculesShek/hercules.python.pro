#coding=utf-8 
import MySQLdb

conn=MySQLdb.connect(host="localhost",user="root",passwd="xrt512",db="hz_bus",port=3306)
cur = conn.cursor();

#创建alphaTable3
cur.execute(u'''
create table alphaTable3
as select * from 
(
select stopInfo,AVG(internalTime) as averageInternalTime,timeIndex,dayType,quarter,
100.00/100 as cfftOfVar
from alphaTable1
group by stopInfo,timeIndex,dayType,quarter
)
as t''')
conn.commit()

#计算alphaTable1中的平均值并更新alphaTable3中的averageInternalTime，主要是过滤数据
cur.execute(u'''select distinct stopInfo,timeIndex,dayType, quarter from alphaTable1''')
groups = cur.fetchall()

sql = '''SELECT distinct stopInfo,internalTime,timeIndex,dayType,quarter FROM hz_bus.alphaTable1'''
cur.execute(sql)
resList = cur.fetchall()
resList = list()
'''
stopInfo,   0
timeIndex,  1
dayType,    2
quarter     3
'''
for g in groups:
      t=sorted([resList.pop(resList.index(elem)) for elem in resList \
            if elem[0]==g[0] and elem[2]==g[1] and elem[3]==g[2] and elem[4]==g[3]],key=lambda e:e[1])
      t=t[int(round(len(t)*0.03)):int(round(len(t)*0.97))]
      g=list(g)
      g.insert(0,sum([e[1] for e in t])/len(t))
      params=tuple(g)
      sql=u'''update hz_bus.alphaTable3 set averageInternalTime = %d
              where stopInfo like '%s' and timeIndex=%d and dayType=%d and quarter=%d''' % params
      cur.execute(sql)
      conn.commit()
#计算变化系数
cur.execute('''
update hz_bus.alphaTable3 as t1,
	    (
	    select b.stopInfo,
		  b.timeIndex,b.dayType,b.quarter,b.averageInternalTime*1.00/a.averageInternalTime as factor
	    from hz_bus.alphaTable3 a, hz_bus.alphaTable3 b
	    where 
	    a.stopInfo = b.stopInfo and 
	    a.timeIndex = b.timeIndex-1 and 
	    a.dayType = b.dayType and 
	    a.quarter = b.quarter
	    ) as t2
set t1.cfftOfVar = t2.factor
where
	  t1.stopInfo = t2.stopInfo and 
	  t1.timeIndex = t2.timeIndex and 
	  t1.dayType = t2.dayType and 
	  t1.quarter = t2.quarter

''')
conn.commit()
conn.close()








