import collections
import threading
import time
candle=collections.deque(xrange(5))
def burn(direction, nextSource):
    while True:
        try:
            next=nextSource()
        except IndexError:
            break
        else:
            print '%s : %s' % (direction, next)
            time.sleep(1)
    print "done %s" % direction
    return
left=threading.Thread(target=burn, args=('left', candle.popleft))
right=threading.Thread(target=burn, args=('left2', candle.popleft))

left.start()
right.start()

left.join()
right.join()
