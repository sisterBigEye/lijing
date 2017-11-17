#-*- coding:utf-8 -*-
from selenium import webdriver
import csv
import time
import codecs
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

driver = webdriver.Chrome()
# url='http://www.gsxt.gov.cn/%7BwmIciRkKOcJMhYgFFkT2VMRCd65RiZ23vLlZnyuy4g1Ey-qz32VVsSFRzAwBvGWuLpd50aaNHGpieDELVNJga2I6i_vZi8HO3Q6j8IFqotaBCjV3bCisgExCQMZ0P0Fh-1509066083116%7D'
url = 'http://www.gsxt.gov.cn/%7BimRcfHpKaE8p7LCOSv9kebXUHBLVsynO2UKEYnbqac_vHC8UXwKek5Lnjzon7OLMUx7JfkgM3BJsh4J9f6y_Bk6buN1OXCiq6DX2IF7NTS66iKDhMX1tYzFdouq_3KjR-1510645611449%7D'
driver.get(url)
if driver.current_url=='http://www.gsxt.gov.cn/index/invalidLink':
    pass
else:
    #留出页面加载时间
    time.sleep(10)
    #窗口向下滚动
    driver.execute_script("window.scrollBy(0,3000)")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,5000)")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,7000)")
    time.sleep(1)

def stock_change_info():
    total=[]
    more_hh=[]
    name=['sort_n','shareholder','Be_percent','Af_percent','change_date','pub_data','social_unique_code']
    # driver[k%len(driver)].get(url[k])
    #得到总页数
    try:
        ye = driver.find_element_by_xpath('//*[@id="needPaging_change_info"]').text

        ye_num= re.findall(r'\d+',ye)[1]
    except:
        ye_num=0
    for h in range(int(ye_num)):
        if ye_num==0:
            break
        #取得所有原始列表数据
        for i in range(1,6):
            result={'sort_n':'null','shareholder':'null','Be_percent':'null','Af_percent':'null','change_date':'null','pub_data':'null','social_unique_code':'null'}
            for j in range(1,7):
                try:
                    result[name[j-1]] =driver.find_element_by_xpath('//*[@id="needPaging_change"]/tbody/tr[%d]/td[%d]'%(i,j)).text
                except:
                    break
            if result=={'sort_n':'null','shareholder':'null','Be_percent':'null','Af_percent':'null','change_date':'null','pub_data':'null','social_unique_code':'null'}:break
            result[name[6]]=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
            # print result[name[1]]
            total.append(result)
        #向右滚动
        driver.execute_script('window.scrollBy(100,0)')
        #取出每一行第二个字段中的扰乱符

        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="needPaging_change_next"]').click()
        time.sleep(10)

    with codecs.open('skci.csv','a+','utf-8') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=name)
        for i in range(len(total)):
            writer.writerow(total[i])
        print total
    return total

stock_change_info()

driver.close()

