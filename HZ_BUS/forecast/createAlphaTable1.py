#coding=utf-8
import MySQLdb, urllib2, json
import datetime, time

'''计算一个时刻的timeIndex'''
def timeIndex(t):
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

# dayTypes = {0:u"工作日",1:u"休息日",2:u"节假日" }
dayTypeUrl="http://www.easybots.cn/api/holiday.php?d=%s"

def dayType(day,maxTryNum=5):
      '''获取一个时间的天类型：  {0:u"工作日",1:u"休息日",2:u"节假日" } 
      这个时间的格式必须是 '20130201' 的八位数字'''
      for ttry in range(maxTryNum):
            try:
                  jsonStr = urllib2.urlopen(dayTypeUrl % day).read()
                  break
            except:
                  if ttry<maxTryNum-1:
                        continue
                  else:
                        return 0
      decodejson = json.loads(jsonStr)
      return decodejson[day]

def quarter(t):
      '''获取一个时间所在的季度'''
      return (t.month-1)/3+1

conn=MySQLdb.connect(host="localhost",user="root",passwd="xrt512",db="hz_bus", port=3306)
cur = conn.cursor();

'''get all days'''
cur.execute("SELECT distinct DATE_FORMAT(time, '%Y%m%d') FROM hz_bus.basicstop")
days=cur.fetchall()
dayTypeDict={}
for d in days:
      dayTypeDict[d[0]]=dayType(d[0])

'''fetch all tids'''
cur.execute("SELECT  distinct tid FROM hz_bus.basicstop")
tids = cur.fetchall()

'''fecth all data'''
rsql = '''SELECT DISTINCT a.lineid,a.linedir,a.tid,a.runIndex,a.stopIndex,a.time,b.stopID 
      FROM hz_bus.basicStop a, hz_bus.line2stop b
      WHERE a.lineid = b.lineIdBus AND a.stopIndex = b.stopIndex AND a.linedir = b.lineDirect
      AND tid = %d
      ORDER BY runIndex, TIME'''

'''
lineid,	    0
linedir,    1
tid,	    2     
runIndex,   3	  
stopIndex,  4     
time	    5
stopID      6     cat
'''


baseSql = u"insert into hz_bus.alphaTable1 values (%d,%d,%d,%d,%d,%d,'%s',%d,%d,%d,'%s',%s,%d)"
for tid in tids:
      resSQL = rsql % tid
      cur.execute(resSQL)
      resList = cur.fetchall()
      t = list(resList)

      for a in t:
            currIndex = t.index(a)
            if a[4] == 1:
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


