#-*- coding:utf-8 -*-
import requests
import hashlib
import re
import MySQLdb
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import codecs
import sys
#调用hashlib里的md5()生成一个md5 hash对象
# m=hashlib.md5()#如果是对一条字符串进行处理，可以print hashlib.new("md5", "Nobody inspects the spammish repetition").hexdigest()
# #生成hash对象后，就可以用update方法对字符串进行md5加密的更新处理
# m.update('http://www.cbrc.gov.cn/chinese/home/docView/xzcf_12E261D4B6BB4EAC88814F839D7F6984.html')
# #加密后的十六进制结果，二进制结果digest()
# print m.hexdigest()
# #继续调用update方法会在前面加密的基础上更新加密
# m.update('http://www.cbrc.gov.cn/chinese/home/docView/D0952CF472AB443486104FB03E6FE862.html')
# m2= m.hexdigest()
# if m1==m2:
#     print "right"
# else:
#     print "gun!"
#

# def compareUrl():
#     pass
reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(host="192.168.80.44", user="root", passwd="ahzx2016", port=3306, charset='utf8',db='lijing')
cur = conn.cursor()

def urlitems(fyurl):
    urlz=[]
    for i in range(len(fyurl)):

        HEADERS = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' #模拟登陆的浏览器
                   }
        # driver=webdriver.Chrome()
        # print driver.get(url)

        # res=requests.get(url)
        res= requests.post(fyurl[i],headers=HEADERS)

        soup=BeautifulSoup(res.text,'html.parser')
        # print soup.prettify()
        # print  soup.select('.STYLE8')

        for news in soup.select('.STYLE8'):
            if re.search(ur'处罚信息公开表',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urlz.append(a)
        # print  urlz

    #行政处罚的格式化具体url,并且通过md5加密后写入csv文件
    urls=[]
    urlshash=[]
    xingzhengchufaurl='http://www.cbrc.gov.cn{}'
    #with open('urls.csv','a+') as csvfile:
        # csvfile.seek(0)
        # m1= csvfile.read()
        # print m1
    #第一次与旧的url作对比,取出数据库中第一个url，与手动给出第一次存入url的第一MD5编码对比，若是真就是第一次，否则不是第一次
    cur.execute("SELECT urlhs FROM yjfj_url LIMIT 0,1")
    m=cur.fetchone()
    #fetchaone返回的是一个tuple
    print type(m[0])
    if m[0]==u'4444b05ee8d322996263672ed00b9f85':##这个字符串根据具体数据库改变
        cur.execute("SELECT urlhs FROM yjfj_url LIMIT 0,1")
        m1=(cur.fetchone())[0]
    else:
        cur.execute("SELECT urlhs FROM yjfj_url  ORDER BY id DESC ;")
        m1=(cur.fetchone())[0]
    print m1
    for i in range(len(urlz)):
       # urls.append( hashlib.new('md5',xingzhengchufaurl.format(urlz[i])).hexdigest())
    #做对比
       m2=hashlib.new('md5',xingzhengchufaurl.format(urlz[i])).hexdigest()
       print m2
       if m1==m2: #csvfile.readline()==hashlib.new('md5',xingzhengchufaurl.format(urlz[i])).hexdigest():
           print"没有更新了"
           break
       else:
           #新增数据的url列表
           urls.append(xingzhengchufaurl.format(urlz[i]))
           urlshash.insert(0,m2)

    for i in range(len(urlshash)):
        cur.execute("INSERT INTO yjfj_url (urlhs) VALUES ('%s')"%urlshash[i])
    cur.close()
    conn.close()
    return urls


def fenye(fenyeurl,n):
    fenyeurls=[]
    for i in range(1,n):
        fenyeurls.append(fenyeurl.format(i))
    return fenyeurls

#fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current={}'
fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current={}'
driver=webdriver.Chrome()

def timesf(str1):
    s=re.findall(r'\d+',str1)
    time1=''
    for i in range(len(s)):
        time1=time1+s[i]+'-'
    time1=time1.rstrip('-')
    return time1


def yjfj(url):
    data=[]
    num_retries=2
    for i in range(len(url)):

        driver.get(url[i])
        time.sleep(1)
        try:
            tbody= driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody').text
        except:
            try:
                tbody=driver.find_element_by_css_selector('.n_w > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1)').text
            except:
                tbody=''
        #判断10行和8行的区别
        try:
            r10=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(2)').text
        except:
            r10=''

        name=[u'文书标题',u'公示日期',u'详情url',u'决定书文号',u'被处罚个人姓名',u'被处罚个人单位',u'被处罚机构名称',u'机构负责人',u'案由',u'处罚依据',u'处罚内容',u'做出处罚机构的名称',u'处罚日期']

        result={}
        #是十行
        if not re.search(ur'个人姓名|个人姓|个人名称',tbody) and re.search(ur'主要负责人|法定代表人',tbody) and r10:
            result[name[2]]=url[i]
            try:
                header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                result[name[1]]=re.findall(ur'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
            except:
                result[name[1]]=''
            try:
                result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
            except:
                result[name[3]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)')[0].text
            try:
                result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4)').text
            except:
                result[name[4]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4)')[0].text
            try:
                result[name[5]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text
            except:
                result[name[5]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)')[0].text
            try:
                result[name[6]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)').text
            except:
                result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)')[0].text
            for i in range(7,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-2)).text.replace(' ','')
                except:
                    result[name[i]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-2))[0].text.replace(' ','')#替换点文字前面的空格
            result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
            result[name[12]]=timesf(result[name[12]])
            data.append(result)
        elif re.search(ur'个人姓名|个人姓|个人名称',tbody) and re.search(ur'主要负责人姓名|法定代表人',tbody) :#没有处罚个人的单位9行
            try:#测试tr2,td3中有没有元素，并给出元素。
                t1=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)')
            except:
                try:
                    t1=driver.find_element_by_css_selector('.Section0 > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)')
                except:
                    try:
                        t1=driver.find_element_by_css_selector('.Section0 > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)')
                    except:
                        try:#许昌和枣庄
                            t1=driver.find_element_by_css_selector('.MsoTableGrid > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)')
                        except:
                            t1=''

            try:#测试tr2,td3中有没有元素，并给出元素。如果一个元素是不能.text获取的,这个元素存在，但是text为空，所以做两次判断，判断元素存在吗，再判断元素是什么
                tt1=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
            except:
                try:#海东的情况
                    tt1=driver.find_element_by_css_selector('.Section0 > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                except:
                    try:
                        tt1=driver.find_element_by_css_selector('.Section0 > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                    except:
                        try:#许昌和枣庄
                            tt1=driver.find_element_by_css_selector('.MsoTableGrid > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                        except:
                            tt1=''

            try:#测试tr4,td2中有没有元素，并给出元素。
                t2=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)')
            except:
                t2=''
            try:#测试tr4,td2中有没有元素，并给出元素。
                tt2=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)').text
            except:
                tt2=''
            #处理多一空行的情况，第二行，取不到头元素‘被处罚’。。。。
            try:
                if re.search(ur'被处罚',driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)').text):
                    t3=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)').text
            except:
                try:
                    t3=driver.find_element_by_css_selector('.Section0 > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)').text
                except:
                    try:
                       t3=driver.find_element_by_css_selector('.Section0 > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)').text
                    except:
                        try:
                            t3=driver.find_element_by_css_selector('.MsoTableGrid > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)').text
                        except:
                            try:#海南的情况
                                if re.search(ur'被处罚',driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(1)').text):
                                    t3=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(1)').text
                                elif re.search(ur'被处罚',driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1)').text):
                                    t3=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1)').text
                            except:
                                t3=''
            #正常情况的t1中的不应该是名称
            if t1 and re.search(ur'被处罚',t3) and not re.search(ur'名称',tt1):
                #加入最后页部分榆林的特殊情况，t11,有就做下面，否则做else后面的
                try:
                    t11=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)')
                except:
                    t11=''#假
                if t11:
                    result[name[2]]=url[i]
                    try:
                        header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                        result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                    except:
                        result[name[1]]=''
                    try:
                        result[name[3]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        result[name[3]]='11null'

                    try:
                        result[name[4]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        result[name[4]]='11null'
                    result[name[5]]='11null'
                    try:
                        result[name[6]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        result[name[6]]='11null'
                    try:
                        result[name[7]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text
                    except:
                        result[name[7]]='11null'

                    for i in range(8,len(name)):
                        try:
                            result[name[i]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(3) > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-5)).text
                        except:
                            result[name[i]]='11null'
                    try:
                        result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                    except:
                        result[name[0]]=u'行政处罚信息公开表'
                    result[name[12]]=timesf(result[name[12]])
                else:
                    result[name[2]]=url[i]
                    try:
                        header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                        result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                    except:
                        result[name[1]]=''
                    try:
                        result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        try:
                            result[name[3]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                        except:
                            try:
                                 result[name[3]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                            except:
                                try:
                                    result[name[3]]=driver.find_element_by_css_selector('.MsoTableGrid > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                                except:
                                    result[name[3]]='1null'
                    try:
                        result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                    except:
                        try:
                            result[name[4]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                        except:
                            try:
                               result[name[4]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                            except:
                                try:
                                    result[name[4]]=driver.find_element_by_css_selector('.MsoTableGrid > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                                except:
                                    result[name[4]]='1null'

                    result[name[5]]='1null'

                    try:
                        result[name[6]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3)').text
                    except:
                        try:
                            result[name[6]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3)').text
                        except:
                            try:
                               result[name[6]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3)').text
                            except:
                                try:
                                    result[name[6]]=driver.find_element_by_css_selector('.MsoTableGrid > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3)').text
                                except:
                                    result[name[6]]='1null'
                    for i in range(7,len(name)):
                        try:
                            result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-3)).text
                        except:
                            try:
                                result[name[i]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-3)).text
                            except:
                                try:
                                    result[name[i]]=driver.find_element_by_css_selector('.Section0 > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-3)).text
                                except:
                                    try:
                                        result[name[i]]=driver.find_element_by_css_selector('.MsoTableGrid > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-3)).text
                                    except:
                                        result[name[i]]='1null'
                    try:
                        result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                    except:
                        result[name[0]]=u'行政处罚信息公开表'
                    #处理时间
                    # s=re.findall(r'\d+',result[name[12]])
                    # time1=''
                    # for i in range(len(s)):
                    #     time1=time1+re.findall(r'\d+',result[name[12]])[i]+'-'
                    # result[name[12]]=time1.rstrip('-')
                    result[name[12]]=timesf(result[name[12]])
                    data.append(result)
            elif t1 and re.search(ur'被处罚',t3) and re.search(ur'名称',tt1):
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]#findall返回的是一个列表
                except:
                    result[name[1]]=''
                try:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                except:
                    result[name[3]]='null2'

                try:
                    result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4)').text
                except:
                    result[name[4]]='null2'

                result[name[5]]='null2'

                try:
                    result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)')[0].text
                except:
                    result[name[6]]='null2'
                try:
                    result[name[7]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)')[0].text
                except:
                    result[name[7]]='null2'
                for i in range(8,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-3)).text
                    except:
                        result[name[i]]='null2'
                try:
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                except:
                    result[name[0]]=u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
                data.append(result)
            elif (not t1) and re.search(ur'被处罚',t3) and t2 and re.search(ur'个人姓名|个人姓',tt2):
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                except:
                    result[name[1]]=''
                try:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text
                except:
                    result[name[3]]='null3'
                try:
                    result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)').text
                except:
                    result[name[4]]='null3'
                result[name[5]]='null3'
                try:
                    result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3)')[0].text
                except:
                    result[name[6]]='null3'

                for i in range(7,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-1)).text
                    except:
                        result[name[i]]='null3'
                try:
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                except:
                    result[name[0]]=u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
                data.append(result)
            elif (not t1) and  re.search(ur'被处罚',t3) and t2 and not re.search(ur'个人姓名|个人姓',tt2):
                try:#处理一个特殊情况,表格乱(三种，咸阳，丹东，榆林)
                    t11=driver.find_element_by_css_selector('table.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)')
                except:
                    t11=''#假
                if t11:
                     result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                except:
                    result[name[1]]=''
                    try:
                        result[name[3]]=driver.find_element_by_css_selector('table.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        result[name[3]]='null41'

                    try:
                        result[name[4]]=driver.find_element_by_css_selector('table.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        result[name[4]]='null41'
                    result[name[5]]='null41'
                    try:
                        result[name[6]]=driver.find_element_by_css_selector('table.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                    except:
                        result[name[6]]='null41'
                    try:
                        result[name[7]]=driver.find_element_by_css_selector('table.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text
                    except:
                        result[name[7]]='null41'

                    try:
                        result[name[8]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(3) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text
                    except:
                        try:
                            result[name[8]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(4) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text
                        except:
                            try:
                                result[name[8]]=driver.find_element_by_css_selector('table.MsoNormalTable:nth-child(5) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)').text
                            except:
                                result[name[8]]='null41'

                    for i in range(9,len(name)):
                        try:
                            result[name[i]]=driver.find_element_by_css_selector('table.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-5)).text
                        except:
                            result[name[i]]='null41'
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                    result[name[12]]=timesf(result[name[12]])
                else:
                    result[name[2]]=url[i]
                    try:
                        header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                        result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                    except:
                        result[name[1]]=''
                    try:
                        result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)').text
                    except:
                        result[name[3]]='null42'
                    try:
                        result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3)').text
                    except:
                        result[name[4]]='null42'
                    result[name[5]]='null42'
                    try:
                        result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(3)')[0].text
                    except:
                        result[name[6]]='null42'
                    for i in range(7,len(name)):
                        try:
                            result[name[i]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%i)[0].text
                        except:
                            result[name[i]]='null42'
                    try:
                        result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                    except:
                        result[name[0]]=u'行政处罚信息公开表'
                    result[name[12]]=timesf(result[name[12]])
                data.append(result)
            else:
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)
                except:
                    result[name[1]]=''
                try:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                except:
                    result[name[3]]='null5'
                try:
                    result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3)').text
                except:
                    result[name[4]]='null5'
                result[name[5]]='null5'
                try:
                    result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)')[0].text
                except:
                    result[name[6]]='null5'
                for i in range(7,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i+4)).text
                    except:
                        result[name[i]]='null5'
                try:
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                except:
                    result[name[0]]=u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
                data.append(result)
        elif re.search(ur'个人姓名|个人姓|个人名称',tbody) and not re.search(ur'主要负责人|法定代表人',tbody):#7行
            result[name[2]]=url[i]
            try:
                header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
            except:
                result[name[1]]=''
            try:
                result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
            except:
                result[name[3]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)')[0].text
            try:
                result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
            except:
                result[name[4]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)')[0].text
            result[name[5]]='7null'
            # try:
            #     result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]').text
            # except:
            #     result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[3]').text
            result[name[6]]='7null'
            result[name[7]]='7null'
            for i in range(8,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-5)).text
                except:
                    result[name[i]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-5))[0].text
            try:
                result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
            except:
                result[name[0]]=u'行政处罚信息公开表'
            result[name[12]]=timesf(result[name[12]])
            data.append(result)
        elif not re.search(ur'个人姓名|个人姓|个人名称',tbody) and re.search(ur'主要负责人|法定代表人',tbody) and not r10:#8行
            try:
                t=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
            except:
                t=''

            if  t and re.search(ur'名称',t):
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                except:
                    result[name[1]]=''
                try:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                except:
                    result[name[3]]='81null'
                result[name[4]]='81null'
                result[name[5]]='81null'
                try:
                    result[name[6]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4)').text
                except:
                    result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4)')[0].text

                for i in range(7,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-4)).text
                    except:
                        result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-4))[0].text
                try:
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                except:
                    result[name[0]]=u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
            elif t and not re.search(ur'名称',t) :
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                except:
                    result[name[1]]=''
                try:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                except:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)')[0].text
                result[name[4]]='8null2'
                result[name[5]]='8null2'
                try:
                    result[name[6]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)').text
                except:
                    result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)')[0].text
                for i in range(7,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-4)).text
                    except:
                        result[name[i]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-4))[0].text
                try:
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                except:
                    result[name[0]]=u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
            else:
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                except:
                    result[name[1]]=''
                try:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                except:
                    result[name[3]]='8null3'
                result[name[4]]='8null3'
                result[name[5]]='8null3'
                try:
                    result[name[6]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)').text
                except:
                    result[name[6]]='8null3'
                for i in range(7,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%(i-4)).text
                    except:
                        result[name[i]]='8null3'
                result[name[0]]= result[name[11]]+u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
            data.append(result)
        else:
            pass
    return data

def newadd_urldetail(urls):

    #调用上面的函数，得到新增数据
    newall_d=[]
    newall_d.extend(yjfj(urls))

    print newall_d
    with codecs.open('newdaa_jyfj.csv','a+','utf-8') as csvfile:
        fieldnames=[u'文书标题',u'公示日期',u'详情url',u'决定书文号',u'被处罚个人姓名',u'被处罚个人单位',u'被处罚机构名称',u'机构负责人',u'案由',u'处罚依据',u'处罚内容',u'做出处罚机构的名称',u'处罚日期']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        for i in range(len(newall_d)):
            writer.writerow(newall_d[i])

    return newall_d

newadd_urldetail(urlitems(fenye(fenyeurl,2)))
driver.close()