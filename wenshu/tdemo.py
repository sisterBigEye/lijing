#-*- coding:utf-8 -*-
from selenium import webdriver
import time
url='http://wenshu.court.gov.cn/list/list/?sorttype=1&number=2T2YKDTK&guid=3a097a41-7543-75a80188-08fc52f964c2&conditions=searchWord+%E8%92%99%E7%89%9B+AJMC++%E6%A1%88%E4%BB%B6%E5%90%8D%E7%A7%B0:%E8%92%99%E7%89%9B'

driver=webdriver.Chrome()
driver.get(url)
time.sleep(60)
courtdata =driver.find_element_by_xpath('//*[@id="resultList"]/div[1]/table/tbody/tr[2]/td/div').text
print courtdata
court = courtdata.split('    ')[0]
number = courtdata.split('    ')[1]
date = courtdata.split('    ')[2]
print court,number,date

