import pymssql,os

conn=pymssql.connect(host='192.168.2.5',user='sde',password='sde',database='HZ_BUS',charset='utf8')
cur=conn.cursor()
sql='''
SELECT lon,lat
  FROM [HZ_BUS].[dbo].[FcdB_Gps]
  where time between '2013/11/8 9:00:00' and '2013/11/8 9:30:00'
  and tid between 40000 and 50000
'''
cur.execute(sql)
gps=cur.fetchall()
file='d:/gps.txt'
if os.path.exists(file):
    os.remove(file)
f=open(file,'a')
f.write('lon\tlat\r\n')

for g in gps:
    f.write(str(g[0])+'\t'+str(g[1])+'\r\n')
f.close()y
