#-*- coding: utf-8 -*-
import MySQLdb
from datetime import datetime
from Queue import Queue
import threading, time
from random import random

conn = MySQLdb.connect(host='localhost', user='root', passwd='xrt512', db='hz_bus', port=3306)
conn.set_character_set('utf8')
cur = conn.cursor()
sql = 'insert into hz_bus.line2stop(lineIdBus,stopIndex,lineDirect,stopID,stopName) \
                               values (%d,%d,%d,%d,\'%s\')'

stopIDs = [256,259,145,123,158,126,147,175,186,102,106,25,6,896,139,945,875,826,445,883]
stopIDs2 = [e+1 for e in stopIDs]

for i, item in enumerate(stopIDs):
      params = (999, i+1, 1, item, u'张家口'+str(item))
      cs = sql % params
      print cs
      cur.execute(cs)

for i, item in enumerate(stopIDs2):
      params = (999, i+1, 2, item, u'张家口'+str(item))
      cs = sql % params
      cur.execute(cs)
