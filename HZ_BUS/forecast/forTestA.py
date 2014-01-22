#coding=utf-8
import DBSupport_ms
from datetime import datetime

def forTestA():
      destBusPass=[(9,5,9),(9,15,3),(9,21,54),(9,30,21),(9,34,29)]
      passed= [(8,35,1),(8,38,45),(8,43,21),(8,50,14),(8,54,2),(8,57,3),(9,5,5),(9,11,22),(9,21,1),(9,25,36),(9,30,5),(9,33,53),(9,38,45)]
      dms = DBSupport_ms.DaoSupport('192.168.2.5', 'sde', 'sde', 'HZ_BUS')
      mssql = 'insert into [HZ_BUS].[dbo].[BasicDataStop0](lineid, linedir, tid, runIndex, stopIndex, time)\
              values (%d, %d, %d, %d, %d, \'%s\')'
      for i,t in enumerate(destBusPass):
            params=(999,1,555,7,(i+1),getd(t))
            dms.execOther(mssql, params)
      for i,t in enumerate(passed):
            params=(999,1,666,3,(i+1),getd(t))
            dms.execOther(mssql, params) 
      dms.commit()
      dms.close()

def getd(t):
      prefix = [2013,11,20]
      prefix.extend(t)
      d = apply(datetime, prefix)
      return d


if __name__ == '__main__':
      print forTestA()
