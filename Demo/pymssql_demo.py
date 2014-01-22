import pymssql
conn=pymssql.connect(host="192.168.2.5",user="sde",password="sde",database="HZ_BUS",charset="utf8")
cur = conn.cursor();


print conn.autocommit_state

