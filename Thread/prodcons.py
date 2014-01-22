# -*- coding: utf-8 -*-
from random import randint
from time import sleep
from Queue import Queue
from myThread import MyThread

def writeQ(queue):
    print 'producing object for Q...'
    queue.put('MacBook Pro Retina', 1)     
    print "now the size of queue is", queue.qsize()
    
def readQ(queue):
    val = queue.get(1)
    print 'consumed object from Q... size now', queue.qsize()

def writer(queue, loops):#生产者
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1, 3))

def reader(queue, loops):#消费者
    for i in range(loops):
        readQ(queue)
        sleep(randint(2, 5))

funcs = [writer, reader]
nfuncs = range(len(funcs))

def main():
    nloops = randint(2, 5)  #取/放多少次
    q = Queue(32)   #这个q现在是全局的

    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()
        sleep(0.1)

    for i in nfuncs:
        threads[i].join()

    print 'all DONE'

if __name__ == '__main__':
    main()



'''
task1: queue中没有元素，put要5秒才放入，而get现在要取，看看get执行后的时间
task2：put中的timeout参数的意思，是不是超过这个时间就等了
task3：


'''
