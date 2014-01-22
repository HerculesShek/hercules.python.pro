#coding=utf-8
import pymssql, urllib2, json, time

conn=pymssql.connect(host="192.168.2.5",user="sde",password="sde",database="HZ_BUS",charset="utf8")
cur = conn.cursor();

#创建alphaDaysType
cur.execute(u'''
IF EXISTS (
    SELECT  TABLE_NAME FROM HZ_BUS.INFORMATION_SCHEMA.TABLES
    WHERE   TABLE_NAME = 'alphaDaysType')
    DROP TABLE  HZ_BUS.dbo.alphaDaysType;

create table HZ_BUS.dbo.alphaDaysType(
dayValue varchar(8) primary key,
dayType int not null
)
''')
conn.commit()

#dayTypes = {0:u"工作日",1:u"休息日",2:u"节假日" }
dayTypeUrl="http://www.easybots.cn/api/holiday.php?m=%s"
def dayType(month, maxTryNum=5):
    '''获取一个时间的天类型：  {0:u"工作日",1:u"休息日",2:u"节假日" }
这个时间的格式必须是 '20130201' 的八位数字'''
    for ttry in range(maxTryNum):
        try:
            jsonStr = urllib2.urlopen(dayTypeUrl % month).read()
            break
        except:
            if ttry<maxTryNum-1:
                print 'network warning'
                time.sleep(0.3)
                continue
            else:
                return
    decodejson = json.loads(jsonStr)
    return decodejson[month]

class oneYearDays():
    def __init__(self, year):
        self.year = year
        self.isLeapYear(year)
        self.parse()

    def isLeapYear(self, y):
        if y % 100 == 0:
            if y % 400 == 0:
                self.leap = True
            else:
                self.leap = False
        else:
            if y % 4 == 0:
                self.leap = True
            else:
              self.leap = False

    def parse(self):
        self.data = {}
        for i in xrange(12):
            month = "%d%02d" % (self.year, (i+1))
            if i==0 or i==2 or i==4 or i==6 or i==7 or i==9 or i==11:
                for d in xrange(31):    #初始化
                    day = "%s%02d" % (month, (d+1))
                    self.data[day] = 0
                for k, v in dayType(month).items(): #赋值
                    day = "%s%02d" % (month, int(k))
                    self.data[day] = int(v)
            if i==3 or i==5 or i==8 or i==10:
                for d in xrange(30):    #初始化
                    day = "%s%02d" % (month, (d+1))
                    self.data[day] = 0
                for k, v in dayType(month).items(): #赋值
                    day = "%s%02d" % (month, int(k))
                    self.data[day] = int(v)
            if i==1:
                if self.leap:
                    for d in xrange(29):    #初始化
                        day = "%s%02d" % (month, (d+1))
                        self.data[day] = 0
                    for k, v in dayType(month).items(): #赋值
                        day = "%s%02d" % (month, int(k))
                        self.data[day] = int(v)
                else:
                    for d in xrange(28):    #初始化
                        day = "%s%02d" % (month, (d+1))
                        self.data[day] = 0
                    for k, v in dayType(month).items(): #赋值
                        day = "%s%02d" % (month, int(k))
                        self.data[day] = int(v)

daySQL = '''insert into HZ_BUS.dbo.alphaDaysType(dayValue, dayType) values ('%s', %d)'''
def storeFourYears():
    for i in xrange(4):
        y = oneYearDays(2010+i)
        for k, v in y.data.items():
            daySQLR = daySQL % (k, v)
            cur.execute(daySQLR)
        
def main():
    storeFourYears()

if __name__ == '__main__':
    main()
    
conn.commit()
conn.close()

