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
import pandas
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
    # cur.execute("SELECT urlhs FROM yjhjg_url LIMIT 0,1")
    # m=cur.fetchone()
    # #fetchaone返回的是一个tuple
    # print type(m[0])
    # if m[0]==u'2d6a7169444966a22cb3281b91c4bcf5':##这个字符串根据具体数据库改变
    #     cur.execute("SELECT urlhs FROM yjhjg_url LIMIT 0,1")
    #     m1=(cur.fetchone())[0]
    # else:
    cur.execute("SELECT urlhs FROM yjhjg_url  ORDER BY id DESC;")
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
           # urlshash.insert(0,m2)
           urlshash.append(m2)

    # for i in range(len(urlshash)):
    try:
        cur.execute("INSERT INTO yjhjg_url (urlhs) VALUES ('%s')"%urlshash[0])
    except:
        pass
    cur.close()
    conn.close()
    return urls


def fenye(fenyeurl,n):
    fenyeurls=[]
    for i in range(1,n):
        fenyeurls.append(fenyeurl.format(i))
    return fenyeurls

#fenyeurl='http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current={}'
fenyeurl='http://www.cbrc.gov.cn/chinese/home/docViewPage/110002&current={}'
driver=webdriver.Chrome()

def timesf(str1):
    s=re.findall(r'\d+',str1)
    time1=''
    for i in range(len(s)):
        time1=time1+s[i]+'-'
    time1=time1.rstrip('-')
    return time1


def yjhjg(url):
    data=[]
    num_retries=2
    # with codecs.open('bank_punish_yjhjg.csv','a+','utf-8') as csvfile:
    for i in range(len(url)):

        driver.get(url[i])
        time.sleep(1)
        name=[u'文书标题',u'公示日期',u'详情url',u'决定书文号',u'被处罚个人姓名',u'被处罚个人单位',u'被处罚机构名称',u'机构负责人',u'案由',u'处罚依据',u'处罚内容',u'做出处罚机构的名称',u'处罚日期']
        # writer =csv.DictWriter(csvfile,fieldnames=name)
        result={}
        result[name[2]]=url[i]
        try:
            header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
            result[name[1]]=re.findall(ur'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
        except:
            result[name[1]]=''

        try:
            result[name[3]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td[2]/p').text
        except:
            result[name[3]]='null'

        try:
            result[name[4]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]/p').text
        except:
            try:
                result[name[4]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[2]/td[3]/div/p').text
            except:
                result[name[4]]='null'
        result[name[5]]='null'
        try:
            result[name[6]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]/p/span[1]').text
        except:
            try:
                result[name[6]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]/div/p').text
            except:
                result[name[6]]='null'

        for i in range(7,len(name)):
            try:
                result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]' %(i-3)).text.replace('\n','')
            except:
                try:
                   result[name[i]]=driver.find_element_by_xpath('//*[@id="doc"]/center/div[3]/div[1]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/table/tbody/tr[%d]/td[2]/p/span[1]'%(i-3)).text.replace('\n','')
                except:
                    result[name[i]]='null'
        result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
        result[name[12]]=timesf(result[name[12]])
        # writer.writerow(result)
        data.append(result)
    return data

def newadd_urldetail(urls):

    #调用上面的函数，得到新增数据
    newall_d=[]
    newall_d.extend(yjhjg(urls))

    print newall_d
    csvname=time.strftime("%Y%m%d.%H.%M.%S")
    with codecs.open('yjhjg%s.csv'%csvname,'a+','utf-8') as csvfile:
        fieldnames=[u'文书标题',u'公示日期',u'详情url',u'决定书文号',u'被处罚个人姓名',u'被处罚个人单位',u'被处罚机构名称',u'机构负责人',u'案由',u'处罚依据',u'处罚内容',u'做出处罚机构的名称',u'处罚日期']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        #加表头
        # writer.writeheader()
        for i in range(len(newall_d)):
            writer.writerow(newall_d[i])

    return newall_d

newdata=newadd_urldetail(urlitems(fenye(fenyeurl,5)))
# pd = pandas.DataFrame(newdata,columns=['DOC_NAME','PUB_DATE','DETAIL_URL','LETTER','PER_NAME','REVERSE_1','ORG_NAME','ORG_CHARGER','REC_DES','PUN_BASE','PUN_DETAUL','GOV_ORG','PUN_DATE'])
# pd.to_csv('yjhfj_addn.csv')
driver.close()
