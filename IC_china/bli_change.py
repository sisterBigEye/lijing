#-*- coding: utf-8 -*-
__author__ = 'kinglee'




from selenium import webdriver
import time
import MySQLdb
import pandas as pd
from DB import HeroDB
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


#公司的url

url=['http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LgqcfgnsLSxcPXEihDGl8hQjejG3SRUTcFfWd6bSydPpoHPTnWAxqexKeDE-WasXj-1508906634499%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LgqcfgnsLSxcPXEihDGl8hThEvpJrSUinJx4l8gg0EQwopBWJXo3Xk1Rfv4vbi48T-1508901702756%7D','http://www.gsxt.gov.cn/%7BqdH_PipoRkCdzwKXwJkY24miWrPg3gNAQAKHLHZ2mU7hS9kM-04z8xeiVACk0gZAjaZZBt5e47H4WHKxn_BEQuEWeM0DcvlbiqJ-ruL5GNXmtmCuaLEj-V8cApD759ZNNJu-QDjqdCBY2Yxi9Mu5eA-1504241116155%7D','http://www.gsxt.gov.cn/%7BqdH_PipoRkCdzwKXwJkY24miWrPg3gNAQAKHLHZ2mU7hS9kM-04z8xeiVACk0gZAjVijhFm-KGISYzpg3TGGef7abuSBmnZmqo57GVBxvn1veo8ier2Iov_Jbrd8nUZJgtS3iaCs0b_IQP6s5q8f-g-1504241116156%7D']

rowname={u'统一社会信用代码':'social_ucode',u'注册号':'social_ucode',u'类型':'type',u'企业名':'name',u'名称':'name',u'投资人':'investor',u'经营者':'investor',u'法定代表人':'investor',
      u'登记机关':'reg_oran',u'登记状态':'reg_state',u'经营场所':'place',u'住所':'place',u'经营范围':'scope',u'注册日期':'begin_date',u'成立日期':'begin_date',
      u'核准日期':'pess_date',u'注册资本':'invest_money',u'营业期限自':'run_from_date',u'营业期限至':'run_end_data'}

driver = webdriver.Chrome()

def business_licence_info(url):
    #营业执照信息

    # result={}
    result={'social_ucode':'null','type':'null','name':'null','investor':'null','reg_oran':'null','reg_state':'null','place':'null','scope':'null','begin_date':'null','pess_date':'null','invest_money':'null','run_from_date':'null','run_end_data':'null'}

    #用chrome访问url

    driver.get(url)
    if driver.current_url=='http://www.gsxt.gov.cn/index/invalidLink':
        pass
    else:

        # result={'social_ucode':'null','type':'null','name':'null','investor':'null','reg_oran':'null','reg_state':'null','place':'null','scope':'null','begin_date':'null','pess_date':'null','invest_money':'null','run_from_date':'null','run_end_data':'null'}

        #留出页面加载时间
        time.sleep(10)
        #窗口向下滚动
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(1)

        #营业执照信息
        for i in range(1,14):
            # result={'social_ucode':'null','type':'null','name':'null','investor':'null','reg_oran':'null','reg_state':'null','place':'null','scope':'null','begin_date':'null','pess_date':'null','invest_money':'null','run_from_date':'null','run_end_data':'null'}

            try:
                t=driver.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dt'%i).text
                t1=t.replace('：','')
                print t1
                if t1 in rowname.keys():
                    print "yes"
                    print rowname[t1]
                    print "no"
                    result[rowname[t1]] = driver.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dd'% i).text
                else:
                    pass
            except:
                print "hihi"
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
info1=many_company_business_license_info(url)
print info1
# 直观展现数据
d_result = pd.DataFrame(info1)
d_result.to_csv('bli.csv')
# d_result.to_excel('company_info.xlsx')
#得到所给公司的信息集合，是个【{}，{}】
# info1=many_company_business_license_info(url)
#
#
# #取出每个字典中的值,insert用
# data=[]
# for i in range(len(url)):
#     try:
#         data.append(info1[i].values())
#     except:
#         break
#
#
# conn = MySQLdb.connect(host='192.168.60.100', user='root', passwd='ahzx2016', db='test1', port=3306, charset='utf8')
# cur = conn.cursor()
# db=HeroDB('hello', conn, cur)

#插入
# db.insertMore('hello', data)
# #更新
# setstr='%dengji_state=%s,re_p_in_law=%s,est_data=%s,reg_jiguan=%s,scape,from_data=%s,reg_invest=%s,hezhunriqi=%s,end_data=%s,type=%s,companyname=%s,place=%s where socialcode=%s;'
# db.update('yinyezhizhao_info',setstr,data)

# db.createTable_k('hello',info1[0])

driver.close()