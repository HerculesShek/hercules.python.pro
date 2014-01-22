# -*- coding: utf-8 -*-
import threading, time, urllib2, Queue

hosts = ["http://yahoo.com","http://google.com","http://apple.com",\
            "http://ibm.com","http://amazon.com"]

queue=Queue.Queue()

class threadUrl(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
          #grabs host from queue
          host = self.queue.get()
          #grabs urls of hosts and prints first 1024 bytes of page
          url = urllib2.urlopen(host)
          print url.read(1024)
          #signal to queue job is done
          self.queue.task_done()         #当前的任务完成时，将会通知之前的任务

start = time.time()
def main():
   #spawn a pool of threads, and pass them queue instance
   for i in range(5):
      t = threadUrl(queue)
      #t.setDaemon(True)         #设置为守护线程
      t.start()
   #populate queue with data
   for host in hosts:
     queue.put(host)
   #wait on the queue until everything has been processed
   queue.join()     
#在队列中的所有项均执行后，再推出，如果没有这句，函数将立即推出
     #这是join()执行的核心：     while self.unfinished_tasks:
     #                               self.all_tasks_done.wait()
main()
print "Elapsed Time:%s" % (time.time() - start)
