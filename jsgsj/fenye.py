#-*- coding: utf-8 -*-
from selenium import webdriver
import time
import  requests



# #手段搜索获取cookeie,行不通
# saved_cookie = {'BIGipServerpool_gsp=3539904704.24841.0000; JSESSIONID=vcVdZNMYbhwLNvyNGvkJgFnXnxq1h3dsXjxGKSFVyQdW3fxzk9pT!-1294366735'}
#
# driver = webdriver.Chrome()
# driver.get(url)
# # driver.delete_all_cookies()
# for cookie in saved_cookie:
#     driver.add_cookie(cookie)
#
# driver.get(url)
# driver.implicitly_wait(1)
# print driver.get_cookies()
#
#
#
# time.sleep(3)
# cont = driver.find_element_by_id('index').text
# print cont


#试下request保持cookie
#x = requests.session()

url='http://www.jsgsj.gov.cn:58888/province/login.jsp'

driver = webdriver.Chrome()
driver.get(url)
#触发这个验证码后发个报警去手动处理一下.失败了，click（）不成功
#"请输入搜索关键字
print "请输入搜索关键字："
name=raw_input()
driver.find_element_by_id('name').send_keys(name)
driver.find_element_by_id('popup-submit').click()

time.sleep(10)

cont = driver.find_element_by_id('index').text
print cont