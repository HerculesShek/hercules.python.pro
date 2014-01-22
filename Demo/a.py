#！coding=utf8

import urllib2
import cookielib
import httplib
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')] 
urllib2.install_opener(opener)
msg = "<customer><name>xingzhe</name><address>Beijing</address></customer>"

con2 = httplib.HTTPConnection("localhost",8080) #这个地方千万不要加http://！ 详情咨询http://stackoverflow.com/questions/9019134/httpconnection-request-socket-gaierror-in-python
#print help(httplib.HTTPConnection)
#con2.send(msg)
con2.request("POST", "/restdemo03/services/customers/add",body=msg,headers = {"Content-type": "application/xml; charset=UTF-8","Connection":"keep-alive"})

#con2.send(msg)
response = con2.getresponse()

#print response.getheaders()   #输出response的header
print response.read()
con2.close()

