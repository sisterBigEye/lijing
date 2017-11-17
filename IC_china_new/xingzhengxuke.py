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
url = 'http://www.gsxt.gov.cn/%7BD5SOFRFZI3nT6-RAmHia1_a7NuXwxWbrE4gE4oBNgMr4O1Vypkf5j3rcRmLqNO1W1VnH29remHNi3xrqN64SSgG2gPdA4nBanvUZisbvLaaGelpeqHlihgJH6gn-GxfU-1510644263294%7D'
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
    driver.execute_script("window.scrollBy(0,5000)")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,3000)")
    time.sleep(1)
def administrative_licensing():

    total=[]
    more_hh=[]
    name=['sort_num','file_num','file_name',' valid_from',' valid_until','pemiss_oran','pemiss_content','state','detail','social_unique_code']
    # driver[k%len(driver)].get(url[k])
    #得到总页数
    try:
        ye = driver.find_element_by_xpath('//*[@id="needPaging_instantLicensing_info"]').text
        ye_num= re.findall(r'\d+',ye)[1]
    except:
        ye_num=0
    for h in range(int(ye_num)):
        result={'sort_num':'null','file_num':'null','file_name':'null',' valid_from':'null',' valid_until':'null','pemiss_oran':'null','pemiss_content':'null','state':'null','detail':'null','social_unique_code':'null'}
        if ye_num==0:
            print('没有查到行政许可信息')
            break
        #取得所有原始列表数据
        for i in range(1,10):
            #把"更多标签点开"
            try:
               driver.find_element_by_xpath('//*[@id="needPaging_instantLicensing"]/tbody/tr/td[7]/div[1]/a').click()
            except:
                pass
            try:
                result[name[i-1]] =driver.find_element_by_xpath('//*[@id="needPaging_instantLicensing"]/tbody/tr/td[%d]'%i).text.replace(u'收起更多','')
            except:
                break
        if result=={'sort_num':'null','file_num':'null','file_name':'null',' valid_from':'null',' valid_until':'null','pemiss_oran':'null','pemiss_content':'null','state':'null','detail':'null','social_unique_code':'null'}:break
        result[name[9]]=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
            # print result[name[1]]
        total.append(result)
        #向右滚动
        # driver.execute_script('window.scrollBy(100,0)')
        #
        # driver.find_element_by_xpath('//*[@id="needPaging_instantLicensing_next"]/a').click()
        # time.sleep(10)


    with codecs.open('xzxk.csv','a+','utf-8') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=name)
        for i in range(len(total)):
            writer.writerow(total[i])
        print total
    return total

administrative_licensing()

driver.close()
