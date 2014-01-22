# -*- coding: utf-8 -*-
import threading
print help(threading)
lock = threading.Lock()	#Lock对象
lock.acquire()
lock.acquire()  #产生了死琐。
lock.release()
lock.release()
