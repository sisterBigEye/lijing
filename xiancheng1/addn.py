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

reload(sys)
#获得默认编码
print sys.getdefaultencoding()
#设置默认编码
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
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
    cur.execute("SELECT url FROM urltable LIMIT 0,1")
    m=cur.fetchone()
    #fetchaone返回的是一个tuple
    print type(m[0])
    if m[0]==u'03ce3b5deb8544082161b5f8a5cd9436':##这个字符串根据具体数据库改变
        cur.execute("SELECT url FROM urltable LIMIT 0,1")
        m1=(cur.fetchone())[0]
    else:
        cur.execute("SELECT url FROM urltable  ORDER BY id DESC;")
        m1=(cur.fetchone())[0]
    print "是m1", m1
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
        cur.execute("INSERT INTO urltable (url) VALUES ('%s')"%urlshash[i])
    cur.close()
    conn.close()
    print urls
    return urls


def fenye(fenyeurl,n):
    fenyeurls=[]
    for i in range(1,n):
        fenyeurls.append(fenyeurl.format(i))
    return fenyeurls

#fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current={}'
fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current={}'
driver=webdriver.Chrome()
def yinjianju_dl(url):
    data=[]
    # num_retries=2
    for i in range(len(url)):

        driver.get(url)
        time.sleep(1)

        tbody= driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody').text
        name=[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']

        result={}
        if re.search(ur'个人姓名',tbody):
            try:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[4]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[4]/td[2]').text


            try:
                result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[5]/td[3]').text
            except:
                result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[5]/td[3]/div/p').text

            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[6]/td[3]').text
            except:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[6]/td[3]').text


            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %(i+3)).text
                except:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]'%(i+3)).text

            data.append(result)
        else:
            try:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text

            result[name[1]]='null'
            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[4]').text
            except:
                    result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[4]').text

            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %(i-1)).text
                except:
                    try:
                         result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]' %(i-1)).text
                    except:
                        result[name[i]]='null'
            data.append(result)
    return data

def yinjianju_hn(url):
    data=[]
    num_retries=2
    for i in range(len(url)):

        driver.get(url)
        time.sleep(1)

        # tbody= driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody').text
        # name=['行政处罚决定书文号','处罚个人姓名','处罚个人单位','处罚单位名称','处罚单位法定代表人（主要负责人）姓名','主要违法违规事实（案由）','行政处罚依据','行政处罚决定','作出处罚决定的机关名称','作出处罚决定的日期']
        name=[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
        result={}
        #检查tr[4]td[2]里含不含个人姓名
        try:
            t=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[4]/td[2]').text
        except:
            try:
                t=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[4]/td[2]').text
            except:
                t=''
        #没有处罚个人的单位，9行情况。表格标号不同引起，else后面的情况也可以读到tr[4]td[2],但是读的是错误信息：个人姓名。现做匹配，如果不含'个人姓名'就是下面的方法，否则做else
        if not re.search(ur'个人姓名',t):
            try:
                 result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[4]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[4]/td[2]').text

            try:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[5]/td[3]').text
            except:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[5]/td[3]').text
            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[6]/td[3]').text
            except:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[6]/td[3]').text

            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]'%(i+3)).text
                except:
                        result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]'%(i+3)).text
            data.append(result)
        else:
            try:
                 result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[2]').text

            try:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[4]/td[3]').text
            except:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[4]/td[3]').text
            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[5]/td[3]').text
            except:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[5]/td[3]').text

            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]'%(i+2)).text
                except:
                        result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]'%(i+2)).text
            data.append(result)
    return data

def yinjianju_js(url):
    data=[]
    num_retries=2
    for i in range(len(url)):

        driver.get(url[i])
        time.sleep(1)

        tbody= driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody').text
        # name=['行政处罚决定书文号','处罚个人姓名','处罚个人单位','处罚单位名称','处罚单位法定代表人（主要负责人）姓名','主要违法违规事实（案由）','行政处罚依据','行政处罚决定','作出处罚决定的机关名称','作出处罚决定的日期']
        name=[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
        result={}
        #没有处罚个人的单位，7行情况
        if re.search(ur'个人姓名',tbody):
            try:
                 result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text
            except:
                 result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]').text

            try:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]').text
            except:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[3]').text
            result[name[2]]='null'
            # try:
            #     result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]').text
            # except:
            #     result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[3]').text
            result[name[3]]='null'
            result[name[4]]='null'
            for i in range(5,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]'%(i-2)).text
                except:
                        result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]'%(i-2)).text
            data.append(result)
        #江苏只有8行，无个人的情况
        else:
            try:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text

            result[name[1]]='null'
            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[3]').text
            except:
                    result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]').text

            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %(i-1)).text
                except:
                    try:
                         result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]' %(i-1)).text
                    except:
                        result[name[i]]='null'
            data.append(result)
    return data

def yinjianju_jx(url):
    data=[]
    # num_retries=2
    for i in range(len(url)):

        driver.get(url[i])
        time.sleep(1)
        tbody= driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody').text
        # name=['行政处罚决定书文号','处罚个人姓名','处罚个人单位','处罚单位名称','处罚单位法定代表人（主要负责人）姓名','主要违法违规事实（案由）','行政处罚依据','行政处罚决定','作出处罚决定的机关名称','作出处罚决定的日期']
        name=[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
        result={}
        if re.search(ur'个人姓名',tbody):
            try:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]').text


            try:
                result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]').text
            except:
                result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[3]/div/p').text

            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]').text
            except:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[3]').text


            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %i).text
                except:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]'%i).text

            data.append(result)
        else:
            try:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text

            result[name[1]]='null'
            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[4]').text
            except:
                    result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[4]').text

            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %(i-1)).text
                except:
                    try:
                         result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]' %(i-1)).text
                    except:
                        result[name[i]]='null'
            data.append(result)
    return data
def yinjianju_jl(url):
    data=[]
    num_retries=2
    for i in range(len(url)):

        driver.get(url[i])
        time.sleep(1)

        tbody= driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody').text
        # name=['行政处罚决定书文号','处罚个人姓名','处罚个人单位','处罚单位名称','处罚单位法定代表人（主要负责人）姓名','主要违法违规事实（案由）','行政处罚依据','行政处罚决定','作出处罚决定的机关名称','作出处罚决定的日期']
        name=[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
        result={}
        #没有处罚个人的单位，9行情况
        if re.search(ur'个人姓名',tbody):
            try:
                 result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text
            except:
                 result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]/p').text

            try:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]').text
            except:
                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[3]').text
            result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]').text
            except:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[3]').text
            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]'%i).text
                except:
                        result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]'%i).text
            data.append(result)
        else:
            try:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text
            except:
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]').text


            try:
                result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[4]').text
            except:
                    result[name[1]]='null'

            try:
                result[name[2]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[2]').text
            except:
                  try:
                      result[name[2]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[2]').text
                  except:
                      result[name[2]]='null'
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[4]/td[3]').text
            except:
                result[name[3]]='null'
            for i in range(4,len(name)):
                try:
                    result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %(i+1)).text
                except:
                    result[name[i]]='null'
            data.append(result)
    return data

def yinjianju_h(url):
    data=[]
    num_retries=2
    for i in range(len(url)):

        driver.get(url[i])
        time.sleep(2)


        # name=['行政处罚决定书文号','处罚个人姓名','处罚个人单位','处罚单位名称','处罚单位法定代表人（主要负责人）姓名','主要违法违规事实（案由）','行政处罚依据','行政处罚决定','作出处罚决定的机关名称','作出处罚决定的日期']
        name=[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
        result={}

        try:
            result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]').text
        except:
            try:
                #江苏的情况
                result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[2]').text
            except:
                try:
                    #海南的情况
                    result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[4]/td[2]').text
                except:
                    try:
                        result[name[0]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[4]/td[2]').text
                    except:
                        result[name[0]]='null'

        try:
            result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]').text
        except:
            try:
             result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]/div/p').text
            except:
                try:
                   result[name[1]]=driver.find_element_by_xpath(' //*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[3]').text
                except:
                    try:
                        result[name[1]]=driver.find_element_by_xpath(' //*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[3]/p/span[1]').text
                    except:
                        #海南的情况
                        try:
                            result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[5]/td[3]').text
                        except:
                            try:
                                 result[name[1]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[5]/td[3]').text
                            except:
                                result[name[1]]='null'
        result[name[2]]='null'
        try:
            result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]').text
        except:
            try:
                result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]/div/p').text
            except:
                try:
                    result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[3]').text
                except:
                    try:
                        result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[3]/td[3]/p/span[1]').text
                    except:
                        #海南的情况
                        try:
                            result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[6]/td[3]').text
                        except:
                            try:
                                 result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[6]/td[3]').text
                            except:
                                result[name[3]]='null'

        for i in range(4,len(name)):
            try:
                result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %i).text
            except:
                try:
                   result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]/p/span[1]'%i).text
                except:
                    try:
                        result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]' %i).text
                    except:
                        try:
                             result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]/p/span[1]' %i).text
                        except:
                            #海南的情况：
                            try:
                                result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[%d]/td[2]' %(i+3)).text
                            except:
                                result[name[i]]='null'
        data.append(result)
    return data



def newadd_urldetail(fyurl,urls):
    #存放一般情况的url列表
    urlh=[]
    #存放吉林的url
    urljl=[]
    #存放海南的url
    urlhn=[]
    #存放江苏的url
    urljs=[]
    #存放江西的url
    urljx=[]
    #存放大连的url
    urldl=[]
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
        xingzhengchufaurl='http://www.cbrc.gov.cn{}'
        for news in soup.select('.STYLE8'):
            if re.search(ur'处罚信息公开表',news['title']) and not re.search(ur'江苏|大连|吉林|江西|海南',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urlh.append(xingzhengchufaurl.format(a))


            elif re.search(ur'处罚信息公开表',news['title']) and re.search(ur'海南',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urlhn.append(xingzhengchufaurl.format(a))

            elif re.search(ur'处罚信息公开表',news['title']) and  re.search(ur'江苏',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urljs.append(xingzhengchufaurl.format(a))

            elif re.search(ur'处罚信息公开表',news['title']) and  re.search(ur'大连',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urldl.append(xingzhengchufaurl.format(a))

            elif re.search(ur'处罚信息公开表',news['title']) and  re.search(ur'吉林',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urljl.append(xingzhengchufaurl.format(a))

            elif re.search(ur'处罚信息公开表',news['title']) and  re.search(ur'江西',news['title']):
            # if len(news.select('a'))>0:
                a = news['href']#获取href属性值
                # print a
                urljx.append(xingzhengchufaurl.format(a))

    #存放新增一般情况的url列表
    new_urlh=[]
    #存放新增吉林的url
    new_urljl=[]
    #存放新增海南的url
    new_urlhn=[]
    #存放新增江苏的url
    new_urljs=[]
    #存放新增江西的url
    new_urljx=[]
    #存放新增大连的url
    new_urldl=[]

    for i in range(len(urls)):
        if urls[i] in urlh:
            print "is h"
            new_urlh.append(urls[i])
            print new_urlh
        elif urls[i] in urldl:
            new_urldl.append(urls[i])
        elif urls[i] in urlhn:
            new_urlhn.append(urls[i])
        elif urls[i] in urljs:
            new_urljs.append(urls[i])
        elif urls[i] in urljx:
            new_urljx.append(urls[i])
        elif urls[i] in urljl:
            new_urljl.append(urls[i])
    #调用上面的对应函数，得到新增数据
    newall_d=[]
    #没有特殊情况时new_url为空，会产生url不是string错误.下面做个判断
    if new_urldl:
        newall_d.extend(yinjianju_dl(new_urldl))
    if new_urlh:
        newall_d.extend(yinjianju_h(new_urlh))
    if new_urlhn:
        newall_d.extend(yinjianju_hn(new_urlhn))
    if new_urljl:
        newall_d.extend(yinjianju_jl(new_urljl))
    if new_urljs:
        newall_d.extend(yinjianju_js(new_urljs))
    if new_urljx:
        newall_d.extend(yinjianju_jx(new_urljx))
    print len(newall_d)
    with codecs.open('newdaa.csv','a+','utf-8') as csvfile:#设定编码方式
        # fieldnames =['行政处罚决定书文号','处罚个人姓名','处罚个人单位','处罚单位名称','处罚单位法定代表人（主要负责人）姓名','主要违法违规事实（案由）','行政处罚依据','行政处罚决定','作出处罚决定的机关名称','作出处罚决定的日期']
        fieldnames=[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        for i in range(len(newall_d)):
            writer.writerow(newall_d[i])
    return newall_d

newadd_urldetail(fenye(fenyeurl,2),urlitems(fenye(fenyeurl,2)))
driver.close()
