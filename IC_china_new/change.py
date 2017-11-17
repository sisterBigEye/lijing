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
url = 'http://www.gsxt.gov.cn/%7BFUqXU4zGvjPsy4fJLQyesKd6adOe3XW3cVmqkIE-KZliKJVOYp9-Zz9jdZaf2mbt7rc80mtwKiprnH8GoGOe14DhQwpu1adg7fq_bmaGvCsyeO_O6oCmKwdvIffRfGWWlKdpnwg19vFwNiOdPU0TMA-1509328163888%7D'
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
def Shareholder_investment_info():

    total=[]
    more_hh=[]
    name=['sort_n','change_item','Be_data','Af_data','change_date','social_unique_code']
    # driver[k%len(driver)].get(url[k])
    #得到总页数
    try:
        ye = driver.find_element_by_xpath('//*[@id="altInfo_info"]').text
        ye_num= re.findall(r'\d+',ye)[1]
    except:
        ye_num=0
    for h in range(int(ye_num)):
        if ye_num==0:
            break
        #取得所有原始列表数据
        for i in range(1,6):
            result={'sort_n':'null','change_item':'null','Be_data':'null','Af_data':'null','change_date':'null','social_unique_code':'null'}
            for j in range(1,6):

                #把所有的"更多标签点开"
                try:
                   driver.find_element_by_xpath('//*[@id="altInfoBeSubData%d"]/a'%(j-1)).click()
                except:
                    pass
                try:
                   driver.find_element_by_xpath('//*[@id="altInfoAfSubData%d"]/a'%(j-1)).click()
                except:
                    pass
                try:
                    result[name[j-1]] =driver.find_element_by_xpath('//*[@id="altInfo"]/tbody/tr[%d]/td[%d]'%(i,j)).text.replace(u'收起更多','')
                except:
                    break
            if result=={'sort_n':'null','change_item':'null','Be_data':'null','Af_data':'null','change_date':'null','social_unique_code':'null'}:break
            result[name[5]]=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
            # print result[name[1]]
            total.append(result)
        #向右滚动
        driver.execute_script('window.scrollBy(100,0)')
        #取出每一行第二个字段中的扰乱符
        # for i in range(1,6):
        #     try:
        #         huhao=driver.find_element_by_xpath('//*[@id="altInfo"]/tbody/tr[%d]/td[2]/div[1]'% i).text
        #     except:
        #         pass
        #         # try:
        #         #     huhao=driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]/span[1]'% i).text
        #         # except:
        #         #         #非公示项令huhao为空
        #         #         #多行
        #         #     try:
        #         #         driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]' %i)
        #         #         huhao=''
        #         #
        #         #     except:
        #         #     huhao='null'
        #     print huhao
        #     # print "打印每次的符号:"
        #     # print huhao
        #     #把提取到的扰乱符追加到列表里
        #     more_hh.append(huhao)

        driver.find_element_by_xpath('//*[@id="altInfo_next"]/a').click()
        time.sleep(10)
    # print jitichuzhi
    #从第二行开始，股东出资的3位置要提取中文，5位置要提取数字
    with codecs.open('bgxx.csv','a+','utf-8') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=name)
        for i in range(len(total)):

            #把结果内的扰乱符替换成'',再把\t\n都去掉,测试无法读出扰乱符
            # (total[i])[name[2]]=(total[i])[name[2]].replace(more_hh[i],'')
            # print 'haha'
            (total[i])[name[1]] =''.join(re.findall(r'\S+',(total[i])[name[1]],re.M))
            # print (total[i])[name[1]]
            writer.writerow(total[i])
        print total
    return total

Shareholder_investment_info()

driver.close()