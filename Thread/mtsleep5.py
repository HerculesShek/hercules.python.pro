#-*- coding: utf-8 -*-

import threading
from time import sleep, ctime

loops = (4, 2)

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        apply(self.func, self.args)

def loop(nloop, nsec):  #名字是nloop的进程执行nsec秒
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at:', ctime()

def main():
    print 'starting at:', ctime()
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = MyThread(loop, (i, loops[i]),loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()
        sleep(0.01)

    for i in nloops:
        threads[i].join()
    print 'all DONE at:', ctime()
    
if __name__ == '__main__':
    main()
