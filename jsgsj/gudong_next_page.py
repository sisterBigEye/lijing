#-*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

url='http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=78AB4DDC058110BDAA3B82E7C2990A07&id=CDE1AAF36B38E29EFB8A431642FF7A12&seqId=76E2362462970449B97F93D9DD160ABD&activeTabId=&RN=6'

#request.add_header('user-agent','mozilla/5.0')

# data1={'org':'78AB4DDC058110BDAA3B82E7C2990A07',
#    'id':'CDE1AAF36B38E29EFB8A431642FF7A12',
#    'tmp':'76',
#    'regNo':'70983A9F91C0C160B39A6EFA61AF738EBE49A903A27D3FE21DD3D613A274ADFA',
#    'admitMain':'10',
#    'uniScid':'DD022CF1A444AC0FA797F22CCB165341' ,
#    'seqId':'76E2362462970449B97F93D9DD160ABD',
#    'econKind':'200',
#    'pageSize':'5',
#    'cur_page':'2'
#    }
#以json格式post数据
#d=json.dumps(data)
res=requests.get(url)
soup = BeautifulSoup(res,'html.parser')
gudong = soup.select('#gdczlist')
print gudong
#data=urllib2.urlencode(data)
#r=requests.post(url,data=data1)
#print r.text