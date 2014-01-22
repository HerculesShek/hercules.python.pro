#-*- coding: utf-8 -*-
from time import sleep, ctime
from Queue import Queue
from myThread import MyThread

def produce(queue):
      print 'producing a mac at ', ctime()
      sleep(2)
      queue.put('MAC PRO RETINA')
      
      print 'produced a mac for xingzhe'
      sleep(0.1)

def getMyMac(queue):
      print 'I was watting for the mac at', ctime()
      var=queue.get(1)
      sleep(0.3)
      print 'xingzhe: I got', var, 'at', ctime()


funcs = [produce, getMyMac]
nfuncs = range(len(funcs))

def main():
      q = Queue(1)
      threads = []
      for i in nfuncs:
            t = MyThread(funcs[i],(q,),funcs[i].__name__)
            threads.append(t)
      for i in nfuncs:
            threads[i].start()
            sleep(0.1)
      for i in nfuncs:
            threads[i].join()
      print 'Happy!'

if __name__ == '__main__':
      main()
      
