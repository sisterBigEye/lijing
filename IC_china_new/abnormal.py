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
# url = 'http://www.gsxt.gov.cn/%7B5Y30S-rKHzb7uXJJRMyKKBZQpFRyZuUXLLE-P59tJoyKSfe9x5dGRsm4PFbHrGKwWNnAE8ZcnLTqXbk0eb-3TmhWbT2oJYlBo5PlBOCY7vNN5ora08TTCkQGlthotbw5-1509349714711%7D'
url='http://www.gsxt.gov.cn/%7B5Y30S-rKHzb7uXJJRMyKKBZQpFRyZuUXLLE-P59tJoyKSfe9x5dGRsm4PFbHrGKwagpQHoMt-_YMIAAj3vKT484xJ6hWJBgshDPYjDCGP994nPM_qezwRrSGPYABzVym-1509350292521%7D'
driver.get(url)
if driver.current_url=='http://www.gsxt.gov.cn/index/invalidLink':
    pass
else:
    #留出页面加载时间
    time.sleep(10)
    #窗口向下滚动
    driver.execute_script("window.scrollBy(0,3000)")
    time.sleep(1)
def abnormal_info():
    total=[]
    more_hh=[]
    #'sort_n':序号,'in_reason'：列入原因,'in_date'：列入日期,'in_oran'：作出决定机关列入,'out_reason'：移出原因,'out_date'：移出日期,'out_oran'；作出决定机关移出
    name=['sort_n','in_reason','in_date','in_oran','out_reason','out_date','out_oran','social_ucode']
    # driver[k%len(driver)].get(url[k])
    #进入异常项页
    driver.find_element_by_xpath('//*[@id="tab_primary4"]').click()
    time.sleep(3)
    #得到总页数
    try:
        ye = driver.find_element_by_xpath('//*[@id="needPaging_abnormal_info"]').text
        ye_num= re.findall(r'\d+',ye)[1]
    except:
        ye_num=0
    for h in range(int(ye_num)):
        if ye_num==0:
            break
        #取得所有原始列表数据
        for i in range(1,6):
            result={'sort_n':'null','in_reason':'null','in_date':'null','in_oran':'null','out_reason':'null','out_date':'null','out_oran':'null','social_ucode':'null'}
            for j in range(1,8):

                #把所有的"更多标签点开"
                try:
                   driver.find_element_by_xpath('//*[@id="abnormalInSubData%d"]/a'%(j-1)).click()
                except:
                    pass
                try:
                   driver.find_element_by_xpath('//*[@id="abnormalOutSubData%d"]/a"]/a'%(j-1)).click()
                except:
                    pass
                try:
                    result[name[j-1]] =driver.find_element_by_xpath('//*[@id="needPaging_abnormal"]/tbody/tr[%d]/td[%d]'%(i,j)).text.replace(u'收起更多','')
                except:
                    break
            if  result=={'sort_n':'null','in_reason':'null','in_date':'null','in_oran':'null','out_reason':'null','out_date':'null','out_oran':'null','social_ucode':'null'}:break
            result[name[7]]=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
            # print result[name[1]]
            total.append(result)
        #向右滚动
        driver.execute_script('window.scrollBy(100,0)')

        driver.find_element_by_xpath('//*[@id="needPaging_abnormal_next"]').click()
        time.sleep(10)
    # print jitichuzhi
    #从第二行开始，股东出资的3位置要提取中文，5位置要提取数字
    with codecs.open('abno.csv','a+','utf-8') as csvfile:
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

abnormal_info()

driver.close()

