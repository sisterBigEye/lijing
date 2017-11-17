#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas
import time
import re
##对吉林的处理
import requests
from bs4 import BeautifulSoup

def timesf(str1):
    s=re.findall(r'\d+',str1)
    time1=''
    for i in range(len(s)):
        time1=time1+s[i]+'-'
    time1=time1.rstrip('-')
    return time1

def urlitems(fyurl):
    urlz=[]
    for i in range(len(fyurl)):

        HEADERS = {
                    # 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' #模拟登陆的浏览器
                     'User-Agent' : "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
                   }
        # driver=webdriver.Chrome()
        # print driver.get(url)

        # res=requests.get(url)
        res= requests.post(fyurl[i],headers=HEADERS)

        soup=BeautifulSoup(res.text,'html.parser')
        # print soup.prettify()
        # print  soup.select('.STYLE8')

        for news in soup.select('.STYLE8'):
            if re.search(ur'处罚信息公开表|银监罚决字',news['title']) and not re.search(ur'兴安',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urlz.append(a)
        # print  urlz

    #行政处罚的格式化具体url
    urls=[]
    xingzhengchufaurl='http://www.cbrc.gov.cn{}'
    for i in range(len(urlz)):
       urls.append( xingzhengchufaurl.format(urlz[i]))
    return urls



def fenye(fenyeurl,n):
    fenyeurls=[]
    for i in range(100,n):
        fenyeurls.append(fenyeurl.format(i))
    return fenyeurls


# url='http://www.cbrc.gov.cn/chinese/home/docView/xzcf_12E261D4B6BB4EAC88814F839D7F6984.html'
driver=webdriver.Chrome()
def yinjianhuijiguan(url):
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

    print data
    pd=pandas.DataFrame(data)

    pd.to_excel('yinjianju-yjj203.xlsx')
    return data


#phantomjs设置请求头信息
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
# "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
# )
# driver = webdriver.PhantomJS(desired_capabilities=dcap)

# print driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[6]/td[2]/p').text
fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current={}'
yinjianhuijiguan(urlitems(fenye(fenyeurl,203)))

driver.close()




