#-*- coding: utf-8 -*-
__author__ = 'kinglee'




from selenium import webdriver
import time
import MySQLdb
import pandas as pd
from DB import HeroDB
#公司的url

url=['http://www.gsxt.gov.cn/%7BqdH_PipoRkCdzwKXwJkY24miWrPg3gNAQAKHLHZ2mU7hS9kM-04z8xeiVACk0gZAjaZZBt5e47H4WHKxn_BEQuEWeM0DcvlbiqJ-ruL5GNXmtmCuaLEj-V8cApD759ZNNJu-QDjqdCBY2Yxi9Mu5eA-1504241116155%7D','http://www.gsxt.gov.cn/%7BqdH_PipoRkCdzwKXwJkY24miWrPg3gNAQAKHLHZ2mU7hS9kM-04z8xeiVACk0gZAjVijhFm-KGISYzpg3TGGef7abuSBmnZmqo57GVBxvn1veo8ier2Iov_Jbrd8nUZJgtS3iaCs0b_IQP6s5q8f-g-1504241116156%7D']


def business_licence_info(url):
    #营业执照信息

    result={}

    #用chrome访问url

    driver = webdriver.Chrome()
    driver.get(url)
    #留出页面加载时间
    time.sleep(10)
    #窗口向下滚动
    driver.execute_script("window.scrollBy(0,3000)")
    time.sleep(1)


    #营业执照信息
    for i in range(1,14):
        try:
            result[driver.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dt'%i).text] = driver.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dd'% i).text
        except:
            break

    return result

    # info.append(result)
    #
    # return info


#获取批量数据
def many_company_business_license_info(url):
    info=[]
    for i in range(len(url)):
        try:
            time.sleep(10)
            info.append(business_licence_info(str(url[i])))
        except:
            print"获取失败 %d" %i
    return info

##脚本内测试
# def sql_run(sql_sentence):
#     db=MySQLdb.connect(host="192.168.60.100",user="root" ,passwd="ahzx2016",db="test1",charset='utf8')
#     cursor= db.cursor()
#     cursor.execute(sql_sentence)
#     datasource=cursor.fetchall()
#     db.commit()
#     cursor.close()
#     db.close()
#     return datasource
#
#
#
#
#
# print many_company_business_license_info(url)
#
#
# #取出每个字典中的值
# data=[]
# for i in range(len(url)):
#     data.append(info[i].values())
# #插入数据库
# for i in range(len(url)):
#     sql_sentence = "INSERT INTO yinyezhizhao_info VALUES" +"(" + "'"+"','".join(data[i])+"'" ")"
#     print sql_sentence
#     sql_run(sql_sentence)

#直观展现数据
# d_result = pd.DataFrame(info)
# d_result.to_excel('company_info.xlsx')
#得到所给公司的信息集合，是个【{}，{}】
info1=many_company_business_license_info(url)


#取出每个字典中的值,insert用
data=[]
for i in range(len(url)):
    try:
        data.append(info1[i].values())
    except:
        break


conn = MySQLdb.connect(host='192.168.60.100', user='root', passwd='ahzx2016', db='test1', port=3306, charset='utf8')
cur = conn.cursor()
db=HeroDB('hello', conn, cur)

#插入
# db.insertMore('hello', data)
# #更新
# setstr='%dengji_state=%s,re_p_in_law=%s,est_data=%s,reg_jiguan=%s,scape,from_data=%s,reg_invest=%s,hezhunriqi=%s,end_data=%s,type=%s,companyname=%s,place=%s where socialcode=%s;'
# db.update('yinyezhizhao_info',setstr,data)

# db.createTable_k('hello',info1[0])
