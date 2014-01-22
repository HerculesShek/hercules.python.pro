#-*- coding: utf-8 -*-
from datetime import datetime
from Queue import Queue
from myThread import MyThread
import threading, time
from random import random

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
            print 'Going is done'
            for t in self.threads:
                  t.join()
                  
      def transferRunTime(self, t):
            '''将程序中的时间戳转换为事实的时间 '''
            secondsFromStartTime = (t-self.baseTime)*timeFactor
            currTimestamp = time.mktime(self.startTime.timetuple())+secondsFromStartTime
            return datetime.fromtimestamp(currTimestamp)

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
                  
if __name__ == '__main__':
      stationQ1 = Queue()
      stationQ2 = Queue()

      baseTid = 90000
      for i in xrange(9):
            baseTid += 1
            t = (baseTid, 1)
            stationQ1.put(t)
      
      for i in xrange(8):
            baseTid += 1
            t = (baseTid, 1)
            stationQ2.put(t)

      going1 = Going(stationQ1,'up',datetime(2013,10,9,6),datetime(2013,10,9,21,30),999,1,stationQ2)
      going2 = Going(stationQ2,'down',datetime(2013,10,9,6),datetime(2013,10,9,21,0),999,2,stationQ1)
      going1.start()
      going2.start()
      going1.join()
      going2.join()
      print 'all done'


      #print help(datetime)
      '''
      timestamp = time.time()
      print timestamp
      print time.ctime(time.time())
      # d = datetime(2013,10, 16)
      d = datetime.fromtimestamp(timestamp)
      #d.seconds
      print d
      print time.mktime(d.timetuple())
      print time.localtime(timestamp)
      print 'localtime type is', type(time.localtime(time.time()))
      '''
  
            
