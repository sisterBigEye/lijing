#-*- coding:utf-8 -*-
from selenium import webdriver

url='http://news.163.com/17/0811/09/CRI3LLHB000189FH.html'
driver=webdriver.Chrome()
driver.get(url)
#获取cookies
cookie = driver.get_cookies()
print cookie

#打印cookies
cookie1 = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
cookiestr = ';'.join(item for item in cookie1)
print cookiestr


savedCookies = driver.get_cookies()

driver2=webdriver.Chrome()
driver2.get(url)
driver2.delete_all_cookies()
for cookie2 in savedCookies:
    driver2.add_cookie(cookie2)

driver2.get(url)
driver.implicitly_wait(1)
print(driver2.get_cookies())

driver.close()
