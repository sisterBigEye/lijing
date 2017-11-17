#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


url='https://hf.fang.anjuke.com/loupan/all/'
res = requests.get(url)
soup=BeautifulSoup(res.text,'html.parser')
print res.text.encode('utf-8')

name=''
place=''
price=''
