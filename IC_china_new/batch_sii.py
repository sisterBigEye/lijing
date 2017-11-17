#-*- coding: utf-8 -*-
__author__ = 'kinglee'

from selenium import webdriver
import time
import pandas
import re
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#代理
# PROXY='117.66.82.37:8118'
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' %PROXY)
url=['http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LgqcfgnsLSxcPXEihDGl8hVjOfyl0CFbX86EyFJ6hpTbYCx0zIHTg0TZUC6UzGCP4-1508915775312%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LytTeyXUVkWArocttMqA6MoiWPKVeP6LLfOPG1b4rmM0opBWJXo3Xk1Rfv4vbi48T-1508916007685%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LytTeyXUVkWArocttMqA6MkWCUBHgLcr7xDLUf7diFsRBJHhLUiSfiB9gA_8TB3MT-1508915905239%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LgqcfgnsLSxcPXEihDGl8hVjOfyl0CFbX86EyFJ6hpTbYCx0zIHTg0TZUC6UzGCP4-1508911189143%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LytTeyXUVkWArocttMqA6MkWCUBHgLcr7xDLUf7diFsRBJHhLUiSfiB9gA_8TB3MT-1508911915425%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LgqcfgnsLSxcPXEihDGl8hczfGcNp8fRnSxE0v7oVxC_YCx0zIHTg0TZUC6UzGCP4-1508895409541%7D','http://www.gsxt.gov.cn/%7BT8ENfEot5pnSCUH8V8SxDc5wo4Tn39gdVm8IDvqpBVT7SFSYxP3GVolslEP92QeIOEpY_TTrAkYPfI0CpbOee43mbS-SWCBNJ7hyGNXNDD69bgTU6yyGUirSva6NOsXveWxqJYZbXaXS5-Xm_XD-YQ-1504509297430%7D']
# url=['http://www.gsxt.gov.cn/index/invalidLink','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LytTeyXUVkWArocttMqA6MkWCUBHgLcr7xDLUf7diFsRBJHhLUiSfiB9gA_8TB3MT-1508893920780%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LytTeyXUVkWArocttMqA6MoiWPKVeP6LLfOPG1b4rmM0opBWJXo3Xk1Rfv4vbi48T-1508895389049%7D','http://www.gsxt.gov.cn/index/invalidLink']
# driver =[webdriver.Chrome(),webdriver.Chrome(),webdriver.Chrome()]
driver = webdriver.Chrome()

def Shareholder_investment_info(url):
    total=[]
    more=[]
    jitichuzhi=[]#具体出资
    for k in range(len(url)):

        t=['sort_n','sh_name','sh_type','certif_type','certif_num','invest_detail(10K)','social_unique_code']
        # driver[k%len(driver)].get(url[k])
        driver.get(url[k])
        if driver.current_url =='http://www.gsxt.gov.cn/index/invalidLink':
            pass
        else:
            time.sleep(10)

            #下拉加载处理
            driver.execute_script('window.scrollBy(0,3000)')
            # driver.maximize_window()
            time.sleep(5)


            # result={}
            try:
                #股东出资表头，测试有没有股东出资表,把字符中的'/'的去掉，否则在建立数据表名时会报错,无表头pass
                 driver.find_element_by_xpath('//*[@id="shareholderInfo"]/thead/tr/th[1]').text
            except:
                #没有表使得表头结果为0
               pass
            #     result={}
            # # print result
            # if result!={}:
            #     result[7]=u'统一社会信用代码'
            # total.append(result)

            # more=[]
            # jitichuzhi=[]
            for h in range(3,8):
                try:
                    #表头追加进了total里面，如果有内容则表示股东出资表存在，否则，不存在

                    num = driver.find_element_by_xpath('//*[@id="shareholderInfo_paginate"]/ul/li[%d]/a' %h).text
                    # print "页数是："
                    # print num
                #num字符数转化成整数
                    if int(num)>=1 and int(num)<10:
                        driver.find_element_by_xpath('//*[@id="shareholderInfo_paginate"]/ul/li[%d]/a' %h).click()
                        time.sleep(10)
                    else:break
                except:
                    break
                #取得所有原始列表数据
                for i in range(1,6):
                    result={'sort_n':'null','sh_name':'null','sh_type':'null','certif_type':'null','certif_num':'null','invest_detail(10K)':'null','social_unique_code':'null'}
                    for j in range(1,7):
                        try:
                            #多行的情况
                            result[t[j-1]] =driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[%d]'%(i,j)).text
                        except:

                            break
                    if result=={'sort_n':'null','sh_name':'null','sh_type':'null','certif_type':'null','certif_num':'null','invest_detail(10K)':'null','social_unique_code':'null'}:break
                    result[t[6]]=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
                    total.append(result)
                #向右滚动
                driver.execute_script('window.scrollBy(1000,0)')
                #取出每一行第五个字段中的扰乱符
                for i in range(1,6):
                    try:
                        huhao=driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]/div[1]'% i).text
                    except:
                        try:
                            huhao=driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]/span[1]'% i).text
                        except:
                                #非公示项令huhao为空
                                #多行
                            try:
                                driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]' %i)
                                huhao=''

                            except:
                                break
                    # print "打印每次的符号:"
                    # print huhao
                    #把提取到的扰乱符追加到列表里
                    more.append(huhao)
                #点击详情查看
                for i in range(1,6):
                    try:
                        #不能做两次点击，这个扰乱符和前一次点击的结果不一致，导致无法匹配
                        #多行的情况
                        driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[6]/span'%i).click()
                        time.sleep(20)
                        try:
                            #有认缴徼用实徼
                            detail =driver.find_element_by_xpath('//*[@id="shareholders_details"]/div[2]/table[2]/tbody/tr[3]').text
                        except:
                            try:
                                #无认缴徼用实徼
                                detail =driver.find_element_by_xpath('//*[@id="shareholders_details"]/div[2]/table[3]/tbody/tr[3]').text
                            except:
                                #认和实信息都没有
                                detail=''
                        driver.find_element_by_xpath('//*[@id="closeColumn"]/p[1]/img').click()
                        time.sleep(3)
                    except:
                        try:
                            driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[6]'%i)
                            detail =''
                        except:
                            break
                    jitichuzhi.append(detail)

    # print jitichuzhi
    #从第二行开始，股东出资的3位置要提取中文，5位置要提取数字
    for i in range(len(total)):
        try:
            (total[i])[t[2]]=''.join(re.findall(ur'[\u4e00-\u9fa5]',(total[i])[t[2]],re.M))
            #清理注册码中的杂数
        except:
            pass
        try:
            #把结果内的扰乱符替换成''
            (total[i])[t[4]]=(total[i])[t[4]].replace(more[i],'')
            #按行读取，取出注册号，把\n\t等去掉,非公示项要直接打印出来

            (total[i])[t[4]] =''.join(re.findall(r'\S+',(total[i])[t[4]],re.M))
            #详情的查看
            #重写详情
            (total[i])[t[5]]=jitichuzhi[i]
            # print (total[i])[5]
            # print (total[i])[6]
        except:
            pass
    print total
    return total

    # #加入社会统一编码
    # for i in range(1,len(total)):
    #     total[i][7]=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span')


total1=Shareholder_investment_info(url)


#直观结果
res=pandas.DataFrame(total1)
res.to_csv('siia.csv')

#数据库表的字段应该是total1[0].values
#insert 数据应该是从total1[1:],第一个数据是字段名称



# #取出每个字典中的值,insert用
# data=[]
# #range从1开始是因为股东信息的第一行是字段名称，这里不需要，真正的股东信息从第二行开始，也就是列表里的第二的开始。
# for i in range(1,len(total1)):
#     try:
#         data.append(total1[i].values())
#     except:
#         break
#
#
# conn = MySQLdb.connect(host='192.168.60.100', user='root', passwd='ahzx2016', db='test1', port=3306, charset='utf8')
# cur = conn.cursor()
# db=HeroDB('hello', conn, cur)
#
#
#
#
# # db.createTable_v('hello1',total1[0])
# db.insertMore('hello1', data)


driver.close()