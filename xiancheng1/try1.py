#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

url='http://www.cbrc.gov.cn/chinese/home/docView/A54D6B0ACD28409F85632BC0DE4C8B07.html'
# fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current={}'
# def urlitems(fyurl):
#     urlz=[]
#     for i in range(len(fyurl)):
#
#         HEADERS = {
#                     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' #模拟登陆的浏览器
#                    }
#         # driver=webdriver.Chrome()
#         # print driver.get(url)
#
#         # res=requests.get(url)
#         res= requests.post(fyurl[i],headers=HEADERS)
#
#         soup=BeautifulSoup(res.text,'html.parser')
#         # print soup.prettify()
#         # print  soup.select('.STYLE8')
#
#         for news in soup.select('.STYLE8'):
#             if re.search(ur'处罚信息公开表',news['title']) and not re.search(ur'江苏|大连|吉林|江西|海南',news['title']):
#             # if len(news.select('a'))>0:
#                 a = news['href']#获取href属性值
#                 # print a
#                 urlz.append(a)
#         # print  urlz
#
#     #行政处罚的格式化具体url
#     urls=[]
#     xingzhengchufaurl='http://www.cbrc.gov.cn{}'
#     for i in range(len(urlz)):
#        urls.append( xingzhengchufaurl.format(urlz[i]))
#     return urls



# def fenye(fenyeurl):
#     fenyeurls=[]
#     for i in range(1,3):
#         fenyeurls.append(fenyeurl.format(i))
#     return fenyeurls
#
#
# # HEADERS = {
# #                     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' #模拟登陆的浏览器
# #
# #                  }
# def find_title(urls):
#     title1=[]
#     url1=[]
#     for i in range(len(urls)):
#         driver.get(urls[i])
#         title=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text  # .lstrip(u'发布时间 : ').rstrip(u'   文章来源 : 吉林   文章类型 : 原创 ')
#         title1.append(re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',title))
#         url1.append(urls[i])
#     print title1,url1

# res= requests.post(url,headers=HEADERS)
#
# soup=BeautifulSoup(res.text,'html.parser')
#
driver = webdriver.Chrome()
driver.get(url)
title=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text  # .lstrip(u'发布时间 : ').rstrip(u'   文章来源 : 吉林   文章类型 : 原创 ')
title1=re.findall(ur'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',title)[0]
print title
print title1
# find_title(urlitems(fenye(fenyeurl)))
driver.close()
# print soup.prettify()
# print  soup.select('.STYLE8')

