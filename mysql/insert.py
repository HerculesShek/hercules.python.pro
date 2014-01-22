import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='xrt512', db='hz_bus', port=3306)
cur = conn.cursor()
sql = 'insert into hz_bus.basicstop(lineid,linedir,tid,runIndex,stopIndex,time) \
                               values (%d,%d,%d,%d,%d,\'%s\')'
params = (999,2,90006,3,5,'2013-10-09 06:00:00.960002')
cs = sql % params
print cs
cur.execute(cs)

