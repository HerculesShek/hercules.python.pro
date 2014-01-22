#coding=utf-8
import threading, time, random
count = 0
class Counter(threading.Thread):
    def __init__(self, lock, threadName):
        super(Counter, self).__init__(name = threadName)  #注意：一定要显式的调用父类的初始化函数。
        self.lock = lock
    
    def run(self):
        global count
        self.lock.acquire()
        print self.getName(), 'get the lock'
        time.sleep(0.5)
        for i in xrange(10000):
            count = count + 1
        
        self.lock.release()
lock = threading.Lock()
ts=[]
for i in range(5):
      t = Counter(lock, "thread-" + str(i))
      ts.append(t)
      t.start()
    
for t in ts:	#确保线程都执行完毕
      t.join()
print count
