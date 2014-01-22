#-*- coding: utf-8 -*-
import DBSupport, DBSupport_ms

dao = DBSupport.DaoSupport('localhost', 'root', 'xrt512', 3306, 'hz_bus')
dms = DBSupport_ms.DaoSupport('192.168.2.5', 'sde', 'sde', 'HZ_BUS')
def exportAlphaTable2():
      alphaTable1Res = dao.execQuery('SELECT * FROM alphatable2')
      mssql='insert into [HZ_BUS].[dbo].[alphaTable2] values (%d,%d,\'%s\',%d,%d,%d,%d,%d,%.6f)'
      for a in alphaTable1Res:
            dms.execOther(mssql, a)
      dms.commit()
      dms.close()

def exportAlphaTable3():
      alphaTable1Res = dao.execQuery('SELECT * FROM alphatable3')
      mssql='insert into [HZ_BUS].[dbo].[alphaTable3] values (\'%s\',%d,%d,%d,%d,%.6f)'
      for a in alphaTable1Res:
            dms.execOther(mssql, a)
      dms.commit()
      dms.close()


def main():
      exportAlphaTable2()
      exportAlphaTable3()

if __name__ == "__main__":
      main()
