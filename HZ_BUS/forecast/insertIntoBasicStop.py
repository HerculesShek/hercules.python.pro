#-*- coding: utf-8 -*-
import MySQLdb
from datetime import datetime
from Queue import Queue
import threading, time
from random import random

conn = MySQLdb.connect(host='localhost', user='root', passwd='xrt512', db='hz_bus', port=3306)
conn.ping(True)
cur = conn.cursor()
#cur.execute('set max_allowed_packet=67108864')
sql = 'insert into hz_bus.basicstop(lineid,linedir,tid,runIndex,stopIndex,time) \
                               values (%d,%d,%d,%d,%d,\'%s\')'

timeFactor=60     #本程序中的时间加速因子
stopConut=20      #多少个公交站

class Going(threading.Thread):
      '''startTime和endTime都是真实的时间 '''
      def __init__(self, queue, name, startTime, endTime, lineid, linedir, targetQ):
            threading.Thread.__init__(self)
            self.queue = queue            # 发车队列
            self.name = name              # 发车线程名
            self.startTime = startTime    # datetime 首发时间
            self.endTime = endTime        # datetime 末班时间
            self.lineid = lineid          # 线路号
            self.linedir = linedir        # 上/下行
            self.baseTime = time.time()   # 程序开始执行的时间，是基准时间
            self.lastDepartureTime = 2    # 保留上次的发车时间 TODO datetime
            self.targetQ = targetQ        # 终点站处的发车队列
            self.threads = []             # 本发车站的所有的发车线程，用来join()

      def run(self):
            print 'start going......'
            curr = time.time()
            while curr < (self.baseTime + (self.endTime - self.startTime).seconds / timeFactor):
                  if self.queue.qsize() > 0:
                        departInfo = self.queue.get()
                        #设置本次的发车时间
                        self.lastDepartureTime = self.transferRunTime(time.time())
                        print self.lastDepartureTime,departInfo
                        depart = Departure(self.targetQ,'',departInfo[0], departInfo[1],\
                                           self.lineid, self.linedir, self.startTime, self.baseTime)
                        depart.setDaemon(True)
                        depart.start()
                        self.queue.task_done()
                        self.threads.append(depart)
                        if self.lastDepartureTime.minute%15 != 0:
                              print '发车晚了些'
                              time.sleep((15 - self.lastDepartureTime.minute%15)*60/timeFactor)
                        else:
                              time.sleep(15*60/timeFactor)
                  curr = time.time()
            for t in self.threads:
                  t.join()
            print 'Going is done'
                  
      def transferRunTime(self, t):
            '''将程序中的时间戳转换为事实的时间 '''
            secondsFromStartTime = (t-self.baseTime)*timeFactor
            currTimestamp = time.mktime(self.startTime.timetuple())+secondsFromStartTime
            return datetime.fromtimestamp(currTimestamp)

l = threading.Lock()
class Departure(threading.Thread):
      '''这里的departTime(发车时间 时间戳类型)用程序的时间'''
      def __init__(self, queue, name, tid, runIndex, lineid, linedir, startTime, baseTime):
            threading.Thread.__init__(self)
            self.queue = queue            # 目的地的queue
            self.name = name              # 线程名字
            self.tid = tid                # 送到目的地
            self.runIndex = runIndex      # 加1后送到目的地
            self.lineid =  lineid         # 父线程给的
            self.linedir = linedir        # 父线程给的
            self.startTime = startTime    # datetime  与Going中的startTime相关
            self.baseTime = baseTime      # timestamp

      def run(self):
            for i in range(stopConut):
                  stopIndex = i+1
                  timeToNext = 300*(1+random())/timeFactor #站间用时 -- 程序中
                  #print 'Reaching in', timeToNext
                  time.sleep(timeToNext)
                  currDatetime = self.transferRunTime(time.time())
                  params = (self.lineid, self.linedir, self.tid, self.runIndex, stopIndex, currDatetime)
                  cs = sql % params
                  l.acquire()
                  cur.execute(cs)
                  l.release()
                  #print '线路号',self.lineid, '上下行', self.linedir, '车号：', self.tid, '车次:',self.runIndex, \
                        #'reached at top', stopIndex, 'at', currDatetime
            print 'depart done'
            nextDepartInfo = (self.tid, self.runIndex+1)
            self.queue.put(nextDepartInfo)
            
      def transferRunTime(self, t):
            '''将程序中的时间戳转换为事实的时间 '''
            secondsFromStartTime = (t-self.baseTime)*timeFactor
            currTimestamp = time.mktime(self.startTime.timetuple())+secondsFromStartTime
            return datetime.fromtimestamp(currTimestamp)

def runOneDay(dayStart1, dayEnd1, dayStart2, dayEnd2):
      stationQ1 = Queue()
      stationQ2 = Queue()

      baseTid = 90000
      for i in xrange(10):
            baseTid += 1
            t = (baseTid, 1)
            stationQ1.put(t)
      
      for i in xrange(11):
            baseTid += 1
            t = (baseTid, 1)
            stationQ2.put(t)
      
      going1 = Going(stationQ1,'up',dayStart1,dayEnd1,999,1,stationQ2)
      going2 = Going(stationQ2,'down',dayStart2,dayEnd2,999,2,stationQ1)

      going1.start()
      going2.start()
      
      going1.join()
      going2.join()

      
if __name__ == '__main__':
      #2013-11-11 到 15号
      '''
      for day in xrange(5):
            t = (datetime(2013,11,11+day,6), datetime(2013,11,11+day,21,30),\
                 datetime(2013,11,11+day,6), datetime(2013,11,11+day,21),)
            apply(runOneDay, t)
            '''
      day = 4
      runOneDay(datetime(2013,11,11+day,6), datetime(2013,11,11+day,21,30),\
                 datetime(2013,11,11+day,6), datetime(2013,11,11+day,21))
      conn.close()
      print 'all done'
