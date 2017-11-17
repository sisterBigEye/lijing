#-*- coding:utf-8 -*-
from selenium import webdriver
import time

#url = 'http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=78AB4DDC058110BDAA3B82E7C2990A07&id=61E00E451E63F0C8D608BAEB709119D3&seqId=F72E2A75DADA311CB633AA7A9A396A93&activeTabId=#'
url = 'http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=78AB4DDC058110BDAA3B82E7C2990A07&id=0B73FD4F697D766FC260A7F98158DF4F&seqId=B2E8D39B68DAE84CF6AEA30EDC44E101&activeTabId='
#url='http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=78AB4DDC058110BDAA3B82E7C2990A07&id=463B77CDD1C2894F59D43834E9864DAA&seqId=6C137337B957A4745FE3B81C607684C8&activeTabId='
driver = webdriver.Chrome()
driver.get(url)
time.sleep(30)
#获取主要人员名单


#测试页面能否获取元素并跳转
driver.find_element_by_xpath('//*[@id="zyrygd"]').click()
curpage_url = driver.current_url
print curpage_url
# sreach_window=driver.current_window_handle
# time.sleep(30)
# peoples = driver.find_element_by_xpath('//*[@id="tab_31"]').text
# print peoples
# try:
#     driver.find_element_by_xpath('//*[@id="zyrygd"]').click()
#     curpage_url = driver.current_url
#     print curpage_url
#     sreach_window=driver.current_window_handle  #此行代码用来定位当前页面
#     time.sleep(3)
#     peoples = driver.find_element_by_xpath('//*[@id="tab_31"]').text
#     print peoples
# except:
#     print "没有查看更多标签"
#     peoples = driver.find_element_by_xpath('//*[@id="zyryList"]').text
#     print  peoples
driver.close()