# -*- coding: utf-8 -*-
import pymssql, time

conn=pymssql.connect(host="192.168.2.5",user="sde",password="sde",database="HZ_BUS",charset="utf8")
cur = conn.cursor();

#计算alphaTable1中的平均值并更新alphaTable2中的averageInternalTime
# 先获取所有的groups
cur.execute(u'''select distinct lineid, linedir, internalIndex,timeIndex,dayType, quarter from alphaTable1
where lineid between 1 and 10;''')
groups = cur.fetchall()
tg = len(groups)
print tg


sql = '''SELECT [lineid],[linedir],[tid],[runIndex],[fromStopIndex],[toStopIndex],[stopInfo],
      [internalTime],[internalIndex],[timeIndex],[dayValue],[dayType],[quarter]
      FROM [HZ_BUS].[dbo].[alphaTable1] where lineid between 1 and 10;'''
cur.execute(sql)
resList = cur.fetchall()

'''
lineid,           0
linedir,          1
internalIndex,    2
timeIndex,        3
dayType,          4
quarter           5
'''

ssToExe = []
#logFile = open('d:/sql.txt','a')
begin = time.time()
updateSQL = u'''update [HZ_BUS].[dbo].[alphaTable2] set averageInternalTime = %d
              where lineid=%d and linedir=%d and internalIndex=%d and
              timeIndex=%d and dayType=%d and quarter=%d'''
for g in groups:
      t=sorted([elem for elem in resList \
            if elem[0]==g[0] and elem[1]==g[1] and elem[8]==g[2] and elem[9]==g[3] and \
               elem[11]==g[4] and elem[12]==g[5]],key=lambda e:e[7])
      t=t[int(round(len(t)*0.03)):int(round(len(t)*0.97))]   #去掉前 3% 和后 3% 的极端数据
      gl=list(g)
      gl.insert(0,sum([e[7] for e in t])/len(t))
      updateSQLR = updateSQL % tuple(gl)
      ssToExe.append(updateSQLR)

'''
for s in ssToExe:
      logFile.write(s)
      logFile.write(';\r\n')

logFile.close()'''
print 'total run time is', (time.time()-begin)


