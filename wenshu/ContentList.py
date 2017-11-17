#-*- coding:utf-8 -*-
import requests as req
import pandas as pd
import time
import re
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger1 = logging.getLogger('logger_logger')
logger2 = logging.getLogger('logger_logger.child')
#这是刚才我们通过F12查找到的网页
url='http://wenshu.court.gov.cn/List/ListContent'
#这是页数、程序休息时间的定义和三个空的列表用来装筛选后的数据。
Index=1
SleepNum = 3
dates=[]
titles=[]
nums=[]
print"请输入案件名称"
name='案件名称:'+str(raw_input())
# res1=req.get('http://wenshu.court.gov.cn')
#
# cookies=req.utils.dict_from_cookiejar(res1.cookies)

#循环模块，因为有很多页，当小于这个数时，不断地传数据，相当于点下一页的功能。最后一句的意思是每执行一次，index加1，就是翻到下一页。具体页数也可以用变量实现。
while Index < 3:

    #这是请求头，伪装成浏览器访问网站，以免被网站屏蔽
    my_headers={'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.95 Safari/537.36 Core/1.50.1280.400',}
    # cookies ={'vjkl5':'0902A0FF6C293601071885B50F969EC1E3FB1B42','_gscu_2116842793':'08228524t3xad734','Hm_lvt_3f1a54c5a86d62407544d433f6418ef5':1508228524,'_gscbrs_2116842793':1,'_gscs_2116842793':'08228524hdh38o34|pv:2','Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5':1508228546}

    #如果实在不会设置，可以在文书网上搜索好，再通过F12查看到的内容复制粘贴到代码中'Param':后即可。
    data={'Param':name, 'Index': Index,'Page':5,'Order':'裁判日期','Direction':'asc','vl5x':'9680fb44c2e0a602d48ab430','number':'XEQN98E8','guid':'e0a1b4a7-c7c9-9d20173f-58840511124e' }

    #将网址、请求头、搜索条件等数据上传并取得内容
    r=req.post(url, headers=my_headers, data = data)
    print r.text
    #用 json解码取得的网页内容
    raw=r.json()
    print raw
#用正则表达式将我们需要的内容提取出来，正则表达式真的很有用，要想真正用好westlaw等数据库，这一关也得过
#大意是定义筛选标准，把（“裁判日期”：）后，（'）前的内容截取出来。
    pattern1 = re.compile('"裁判日期":"(.*?)"', re.S)
    date = re.findall(pattern1,raw)
    pattern2 = re.compile('"案号":"(.*?)"', re.S)
    num = re.findall(pattern2,raw)
    pattern3 = re.compile('"案件名称":"(.*?)"', re.S)
    title = re.findall(pattern3,raw)

#把筛选出的数据添加到开始的三个空列表里
    dates+=date
    titles+=title
    nums+=num

#这一行是让程序休息，做事留点余地比较好。通过网页编码可知，文书网是有验证码功能的，如果你抓的太狠中招莫怪。
    time.sleep(SleepNum)
    Index += 1
#这里我们可以看到，从while开始到此，所有的代码都缩进了四个空格。这是因为要告诉电脑，这一段代码构成一个相对独立的组，当index小于123时，不断地从这个组第一句代码执行到最后一句代码，而不涉及到本文涉及的其他代码。

#这里代码又是顶格写。
#用pandas模块将筛选出的内容转成dataframe格式，并保存到Excel。
logger2.debug("it's over  ")
print dates
print nums
# print title

df=pd.DataFrame({'时间':dates,'案号':nums, '案件名称':titles})
df.to_excel('C:\\result.xlsx')


# get the session cookie
# cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
# #print cookie
# print driver.get_cookies()
# cookiestr = ';'.join(item for item in cookie)
# print cookiestr
    # driver.close()

    # driver.close()

# request = urllib2.Request(url1)
# res1=req.get('http://wenshu.court.gov.cn')
# cookies=req.utils.dict_from_cookiejar(res1.cookies)
# print cookies
# request.add_data('guid:8a6c1bf9-ecb3-07aee890-f36a4a50dc6a')
# request.add_header('User-Agent','Mozilla/5.0')
# response = urllib2.urlopen(request)