# -*- coding: utf-8 -*-
import pymssql, threading, time

conn=pymssql.connect(host="192.168.2.5",user="sde",password="sde",database="HZ_BUS",charset="utf8")
conn.autocommit(True)
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

alter table HZ_BUS.dbo.alphaTable2 alter column cfftOfVar numeric(25,13)

''')
conn.commit()

l = threading.Lock()
getGroupSQL = u'''select distinct lineid, linedir, internalIndex,timeIndex,dayType, quarter
                  from [HZ_BUS].[dbo].[alphaTable1]
                  where lineid between %d and %d'''
resSQL = u'''SELECT [lineid],[linedir],[tid],[runIndex],[fromStopIndex],[toStopIndex],[stopInfo],
              [internalTime],[internalIndex],[timeIndex],[dayValue],[dayType],[quarter]
              FROM [HZ_BUS].[dbo].[alphaTable1]
              where lineid between %d and %d'''
updateSQL = u'''update [HZ_BUS].[dbo].[alphaTable2] set averageInternalTime = %d
                where lineid=%d and linedir=%d and internalIndex=%d and
                timeIndex=%d and dayType=%d and quarter=%d'''

begin = time.time()
class Hamal(threading.Thread):
    def __init__(self, lineidFrom, lineidEnd, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.f = lineidFrom
        self.e = lineidEnd

    def run(self):
        groupsSQL = getGroupSQL % (self.f, self.e)
        l.acquire()
        cur.execute(groupsSQL)
        groups = cur.fetchall()
        
        groupResSQL = resSQL % (self.f, self.e)
        cur.execute(groupResSQL)
        resList = cur.fetchall()
        l.release()

        for g in groups:
            t=sorted([resList.pop(resList.index(elem)) for elem in resList \
                    if elem[0]==g[0] and elem[1]==g[1] and elem[8]==g[2] and elem[9]==g[3] and \
                    elem[11]==g[4] and elem[12]==g[5]],key=lambda e:e[7])
            t=t[int(round(len(t)*0.03)):int(round(len(t)*0.97))]   #去掉前 3% 和后 3% 的极端数据
            gl=list(g)
            gl.insert(0,sum([e[7] for e in t])/len(t))
            sql = updateSQL % tuple(gl)
            l.acquire()
            cur.execute(sql)
            l.release()

def main():
    lineidsSQL = '''select distinct lineid from [HZ_BUS].[dbo].[alphaTable1] order by lineid'''
    cur.execute(lineidsSQL)
    lineids = cur.fetchall()
    le = len(lineids)
    threads = []
    for i in xrange(5):
        f = lineids[le*i/5][0]
        e = lineids[le*(i+1)/5-1][0]
        if i == 4:
            e = lineids[-1][0]
        h = Hamal(f, e)
        threads.append(h)
        h.start()
    for t in threads:
        t.join()

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
                  t1.quarter = t2.quarter ''')
    conn.close()
    print 'total time：', (time.time()-begin)

if __name__ == '__main__':
    main()

'''
8115, 'Arithmetic overflow error converting numeric to data type numeric
'''




