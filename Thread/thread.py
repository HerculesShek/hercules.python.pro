#-*- coding: utf-8 -*-
import threading,time
#print help(threading.Thread)

class Producer(threading.Thread):
      
      def __init__(self, t_name):
            threading.Thread.__init__(self)
            self.name=t_name

      def run(self):
            global x
            con.acquire()
            if x>0:
                  con.wait()
            else:
                  for i in range(5):
                        x = x + 1
                        print "Producing......"+str(x)
                        #time.sleep(1)
                  con.notify()
            print x
            con.release()


class Consumer(threading.Thread):
      
      def __init__(self, t_name):
            threading.Thread.__init__(self)
            self.name=t_name

      def run(self):
            global x
            con.acquire()
            if x == 0:
                  print "consumer waiting"
                  con.wait()
            else:
                  for i in range(5):
                        x = x - 1
                        print "cunsuming...."+str(x)
                        #time.sleep(1)
                  con.notify()
            print x
            con.release()

con=threading.Condition()
#print help(con)
x=0
print 'start consumer'
c=Consumer('consumer')
print 'start producer'
p=Producer('producer')
p.start()
c.start()
print 'the name of c is : %s' % c.getName()


