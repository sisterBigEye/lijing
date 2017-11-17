#-*- coding:utf-8 -*-
import urllib2
import requests as req


# url='http://wenshu.court.gov.cn/ValiCode/GetCode'
url='http://wenshu.court.gov.cn/List/ListContent'

data1={'Param':'案件名称:蒙牛',
'Index':1,
'Page':5,
'Order':'法院层级',
'Direction':'asc',
'vl5x':'e0aec5c80ce86eb2c22955f5',
'number':'8CQCY69J',
'guid':'9936ef26-bf32-9468c143-6b8a86aa9b37'}
# request = urllib2.Request(url)
# res1=req.get('http://wenshu.court.gov.cn')
# cookies=req.utils.dict_from_cookiejar(res1.cookies)
# print cookies
# request.add_data('guid:8a6c1bf9-ecb3-07aee890-f36a4a50dc6a')
# request.add_header('User-Agent','Mozilla/5.0')
# response = urllib2.urlopen(request)
# r=req.post(url,data={'Param':'案件名称:蒙牛', 'Index': 1,'Page':5,'Order':'裁判日期','Direction':'asc','guid':'a2f2e98c-a53c-bbe9be82-286ea37fe522','number':'RYRWJ7AD'})
r=req.post(url,data=data1)
print r.text

