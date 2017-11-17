#-*- coding: utf-8 -*-
from selenium import webdriver
import time
import json
import urllib2
# url = 'http://www.jsgsj.gov.cn:58888/province/notice/InformationNotice.jsp'
# driver = webdriver.Chrome()
# driver.get(url)
# time.sleep(3)
# #driver.implicitly_wait(30)
# #cont = driver.find_element_by_xpath('//*[@id="jyycdatas"]/li[1]/a/p[1]/text()')
# #cont = driver.find_element_by_id('jyycdatas').text
# print(driver.get_cookies())
# print ('经营异常名录列入公告').decode('utf-8').encode('gbk')
# print cont
# driver.close()

##如果想用bs4解析网页，可以用WebDriver 的page_source函数返回页面的源代码字符串
# pageSource= driver.page_source
# bsObj = BeautifulSoup(pageSource)
# print(bsObj.find(id='content').get_text())

##获取页面的内容，然后查找隐含链接和隐含输入字段
# from selenium import webdriver
# from selenium.webdriver.remote.webelement import WebElement
#
# driver = webdriver.PhantomJS()
# driver.get('http://pythonscraping.com/pages/itsatrap.html')
# links = driver.find_element_by_tag_name("a")
# for link in links:
#     if not link.is_displayed():
#         print("the link" +link.get_attribute("href")+" is a trap")
#
#
# fields = driver.find_element_by_tag_name("input")
# for field in fields:
#     if not field.is_displayed():
#         print("Do not change value of" +field.get_attribute("name"))
#



#浙江信用信息网
url='http://gsxt.zjaic.gov.cn/pub/infobulletin/list.json?_t=1502164257941&start=0&length=5&params%5BpubType%5D=1&params%5BpubTitle%5D=&params%5BauditArea%5D='
request = urllib2.Request(url)
request.add_header('User-Agent','Mozilla/5.0')
response = urllib2.urlopen(request)
#获取状态码
print response.getcode()
#读取内容
cont = response.read()
time.sleep(10)
cont1 = json.loads(cont)
print cont1

