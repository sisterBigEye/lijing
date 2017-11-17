#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas
import time
import re
import requests
from bs4 import BeautifulSoup
import csv
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


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
            if re.search(ur'处罚信息公开表',news['title']) and re.search(ur'广东',news['title']):
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



def fenye(fenyeurl):
    fenyeurls=[]
    for i in range(1,70):
        fenyeurls.append(fenyeurl.format(i))
    return fenyeurls


# url='http://www.cbrc.gov.cn/chinese/home/docView/xzcf_12E261D4B6BB4EAC88814F839D7F6984.html'
driver=webdriver.Chrome()
def yinjianhuijiguan(url):
    data=[]
    num_retries=2
    with codecs.open('yjj_jl.csv','a+','utf-8') as csvfile:
        for i in range(len(url)):

            driver.get(url[i])
            time.sleep(1)

            tbody= driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody').text
            name=[u'文书标题',u'公示日期',u'详情url',u'决定书文号',u'被处罚个人姓名',u'被处罚个人单位',u'被处罚机构名称',u'机构负责人',u'案由',u'处罚依据',u'处罚内容',u'做出处罚机构的名称',u'处罚日期']
            writer=csv.DictWriter(csvfile,fieldnames=name)
            result={}
            #没有处罚个人的单位，9行情况
            if re.search(ur'个人姓名|个人名称',tbody):
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(ur'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                except:
                    result[name[1]]=''
                try:
                     result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text
                except:
                     result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]/p').text

                try:
                     result[name[4]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]').text
                except:
                     result[name[4]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[3]').text
                result[name[5]]='null'
                try:
                    result[name[6]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]').text
                except:
                    result[name[6]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[3]').text
                for i in range(7,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]'%(i-3)).text.replace('\n','')
                    except:
                            result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]'%(i-3)).text.replace('\n','')
                try:
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                except:
                    result[name[0]]=u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
                writer.writerow(result)
                data.append(result)
            else:
                result[name[2]]=url[i]
                try:
                    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
                    result[name[1]]=re.findall(ur'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
                except:
                    result[name[1]]=''
                try:
                    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)').text
                except:
                    result[name[3]]=''
                result[name[4]]='null'
                result[name[5]]='null'
                for i in range(6,len(name)):
                    try:
                        result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %(i-4)).text.replace('\n','')
                    except:
                        result[name[i]]='null'
                try:
                    result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
                except:
                    result[name[0]]=u'行政处罚信息公开表'
                result[name[12]]=timesf(result[name[12]])
                writer.writerow(result)
                data.append(result)




    print data
    pd=pandas.DataFrame(data)

    pd.to_excel('yinjianju-gd.xlsx')
    return data


#phantomjs设置请求头信息
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
# "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
# )
# driver = webdriver.PhantomJS(desired_capabilities=dcap)

# print driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[6]/td[2]/p').text
fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current={}'
yinjianhuijiguan(urlitems(fenye(fenyeurl)))
