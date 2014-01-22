#!/usr/bin/env python
#coding=utf8

import httplib, urllib

httpClient = None
try:
    params = urllib.urlencode({'name': 'tom', 'age': 22})
    print urllib.urlencode.__doc__
    headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}

    httpClient = httplib.HTTPConnection("localhost", 80, timeout=30)
    httpClient.request("POST", "www.tsnav.cn", params, headers)

    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
    print response.getheaders() #获取头信息
except Exception, e:
    print e
finally:
    if httpClient:
          print httpClient.getresponse
          httpClient.close()
