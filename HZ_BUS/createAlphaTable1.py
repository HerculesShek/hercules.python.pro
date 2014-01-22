#coding=utf-8
import pymssql,urllib2,json
import datetime,time

def timeIndex(t):
      '''计算一个时刻的timeIndex'''
      h = t.hour
      m = t.minute
      if h<6:
            return h
      if h==6:
            return m>=30 and 7 or 6
      if h==7:
            return m/15+8
      if h==8:
            return m<30 and 12 or 13
      if h>=9 and h<16:
            return 5+h
      if h==16:
            return m<30 and 21 or 22
      if h==17:
            return m/15+23
      if h==18:
            return m<30 and 27 or 28
      if h>=19 and h<24:
            return h+10

#dayTypes = {0:u"工作日",1:u"休息日",2:u"节假日" }
dayTypeUrl="http://www.easybots.cn/api/holiday.php?d=%s"

'''
def dayType(day,maxTryNum=5):
      \'''获取一个时间的天类型：  {0:u"工作日",1:u"休息日",2:u"节假日" } 这个时间的格式必须是 '20130201' 的八位数字\'''
      for ttry in range(maxTryNum):
            try:
                  jsonStr = urllib2.urlopen(dayTypeUrl % day).read()
                  break
            except:
                  if ttry<maxTryNum-1:
                        time.sleep(0.2)
                        print 'network warning'
                        continue
                  else:
                        return 0
      decodejson = json.loads(jsonStr)
      return decodejson[day]
'''

conn=pymssql.connect(host="192.168.2.5",user="sde",password="sde",database="HZ_BUS",charset="utf8")
cur = conn.cursor();

dayTypeSQL = u"SELECT [dayType] FROM [HZ_BUS].[dbo].[alphaDaysType] where dayValue = '%s'";
def dayType(day):
      cur.execute(dayTypeSQL % day)
      dayT = cur.fetchone()
      return int(dayT[0]) if dayT is not None else 0

def quarter(t):
      '''获取一个时间所在的季度'''
      return (t.month-1)/3+1

cur.execute("SELECT COUNT(*) FROM [HZ_BUS].[dbo].[FcdB_BasicDataStop]")
itemsCount = cur.fetchone()
print '要处理%d条数据' % itemsCount[0]


begin = time.time()

'''get all days'''
cur.execute("SELECT distinct CONVERT(varchar(12),time,112) FROM [HZ_BUS].[dbo].[FcdB_BasicDataStop]")
days=cur.fetchall()

dayTypeDict={}
for d in days:
      dayTypeDict[d[0]]=dayType(d[0])

print dayTypeDict

'''fetch all tids'''
cur.execute("SELECT distinct tid FROM [HZ_BUS].[dbo].[FcdB_BasicDataStop]")
tids = cur.fetchall()

'''fecth all data'''
rsql = '''select distinct a.lineid,a.linedir,a.tid,a.runIndex,a.stopIndex,a.time,b.stopID 
      from [HZ_BUS].[dbo].[FcdB_BasicDataStop] a, dbo.InfoB_Line2Stop b
      where a.lineid = b.lineIdBus and a.stopIndex = b.stopIndex and a.linedir = b.lineDirect
      AND tid = %d
      ORDER BY runIndex, time'''

'''
lineid,	    0
linedir,    1
tid,	    2     
runIndex,   3	  
stopIndex,  4     
time	    5
stopID      6     cat
'''

baseSql = u"insert into HZ_BUS.dbo.alphaTable1 values (%d,%d,%d,%d,%d,%d,'%s',%d,%d,%d,'%s',%s,%d)"
for tid in tids:
      print 
      resSQL = rsql % tid
      cur.execute(resSQL)
      t = cur.fetchall()
      
      for a in t:
            currIndex = t.index(a)
            if a[4]==1:
                  continue
            if a[4]-t[currIndex-1][4] != 1:
                  continue
            internalTime = (a[5]-t[currIndex-1][5]).seconds
            internalIndex = t[currIndex-1][4]
            tIndex = timeIndex(t[currIndex-1][5]) #时间序列计算的是出站时间
            dayValue = "%d%02d%02d" % (a[5].year,a[5].month,a[5].day)
            dType = dayTypeDict[dayValue]

            values = (a[0],a[1],a[2],a[3],\
                      t[currIndex-1][4],\
                      a[4],\
                      str(t[currIndex-1][6])+'to'+str(a[6]),\
                      internalTime,\
                      internalIndex,\
                      tIndex,\
                      dayValue,\
                      dType,\
                      quarter(a[5]))
            sql = baseSql % values
            cur.execute(sql)
conn.commit()
conn.close()

end = time.time()
print '用时为', (end-begin)

