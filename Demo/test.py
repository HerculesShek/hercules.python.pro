#！coding=utf8

import urllib2
import cookielib
import httplib
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')] 
urllib2.install_opener(opener)
msg = "<xml><ToUserName><![CDATA[gh_3d2ba2b82054]]></ToUserName>\
<FromUserName><![CDATA[oSPGLjr9ZNc6TEIhrV2ltymhSWMI]]></FromUserName>\
<CreateTime>1375087266</CreateTime>\
<MsgType><![CDATA[voice]]></MsgType>\
<MediaId><![CDATA[3jHzMyHLBlgppds4UfT_hPcCrtbi9GiEnu-3z3SHKPij-byYaciWppfeGjsMs9dv]]></MediaId>\
<Format><![CDATA[amr]]></Format>\
<MsgId>5905954836616052755</MsgId>\
<Recognition><![CDATA[]]></Recognition>\
</xml>"
req = urllib2.Request("http://www.tsnav.cn")    #{"username":"root","password":"1234"}
#req.add_data(msg)
#print help(req)
#resp = urllib2.urlopen(req)  
#print resp.read()  
#print urllib2.urlopen("http://www.baidu.com").read()

con2 = httplib.HTTPConnection("www.tsnav.cn")
con2.request("POST", "/",headers = {"Content-Length": 344})

con2.send(msg)
response = con2.getresponse()

print response.getheaders()   #输出response的header
print response.read()
con2.close()

