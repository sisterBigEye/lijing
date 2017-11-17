from selenium import webdriver
import time

url='http://www.cbrc.gov.cn/chinese/home/docView/C9BDB59F519E43579188C5D747B8BBE0.html'
driver = webdriver.Chrome()
driver1 = webdriver.Chrome()
driver.get(url)

# driver.find_element_by_css_selector('.n_w > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > a:nth-child(2)').click()
urla=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[3]/td/a').get_attribute('href')
print(urla)
driver1.get(urla)
time.sleep(10)
t=driver1.find_element_by_xpath('//*[@id="plugin"]').text
print(t)
driver1.close()
driver.close()