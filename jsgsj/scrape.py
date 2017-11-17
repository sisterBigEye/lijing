#-*- coding: utf-8 -*-

import urllib2
#
#
# url = 'http://www.jsgsj.gov.cn:58888/province/NoticeServlet.json?ExceptionNoteList=true'
# request = urllib2.Request(url)
# request.add_header('User-Agent','Mozilla/5.0')
# response = urllib2.urlopen(request)
# #获取状态码
# print response.getcode()
# #读取内容
# cont = response.read()
# print cont

from selenium import webdriver
import time
import pandas as df
import openpyxl
import urllib






#加入代理ip
#PROXY='122.72.32.73:80' #"27.24.48.172:80"#122.72.32.73:80" #IP:PORT or HOST:PORT
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)#chrome_options.add_argument('--proxy-server=http://171.37.135.94:8123')
#driver = webdriver.Chrome(chrome_options=chrome_options)




url='http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=78AB4DDC058110BDAA3B82E7C2990A07&id=CDE1AAF36B38E29EFB8A431642FF7A12&seqId=76E2362462970449B97F93D9DD160ABD&activeTabId='
#url = 'http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=78AB4DDC058110BDAA3B82E7C2990A07&id=A7769DB32056A3EC1D2779D65577525B&seqId=92CFB8E0BD25141A23DF400BBE9F8ADD&activeTabId='
#url='http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=D6CAA68850078FCCB00B65D52F4FF48E&id=61F5025BE6B704A7D2DF850C14F117B1&seqId=55CD45F0906EC0947371AAB2AA1DA5C8&activeTabId='
#url = 'http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=55236E67B5C08FADAC726B3811EAA3CD&id=B4EE79C7C4BF75F7D094689B9EDCA817&seqId=13D17633AEB7D2F9069542C708D0D85F&activeTabId='



driver=webdriver.Chrome()
driver.get(url)
time.sleep(3)
result={}
#企业名
result['title'] = driver.find_element_by_xpath('//*[@id="CORP_NAME"]').text
#driver.implicitly_wait(30)
#cont = driver.find_element_by_xpath('//*[@id="jyycdatas"]/li[1]/a/p[1]/text()')
#cont = driver.find_element_by_id('jyycdatas').text
##获取基本信息
#result['cont'] = driver.find_element_by_id('tab_1_1').text

#获取基本信息内的每个信息

#统一社会信用代码/注册号
result['注册号']=driver.find_element_by_id('REG_NO').text
#公司名称
result['company_name']=driver.find_element_by_id('CORP_NAME').text
#公司类型
result['kind']=driver.find_element_by_id('ZJ_ECON_KIND').text
#公司法定代表人
result['law_man']=driver.find_element_by_id('OPER_MAN_NAME').text
#注册资本
try:
    result['money']=driver.find_element_by_id('REG_CAPI_WS').text
    print "有注册资本信息"
except:
    print "抱歉，没有注册资本信息！"
#成立日期
result['es_date']=driver.find_element_by_id('START_DATE').text
#营业期限自
try:
    result['start_open']=driver.find_element_by_id('FARE_TERM_START').text
except:
    print"没有营业期限自信息"

#营业期限至
try:
    result['end_open']=driver.find_element_by_id('FARE_TERM_END').text
except:
    print"没有营业期限至信息"
#登记机关
result['reg_place']=driver.find_element_by_id('BELONG_ORG').text
#核准日期
result['pemi_date']=driver.find_element_by_id('CHECK_DATE').text
#住所
try:
    result['open_place']=driver.find_element_by_id('ADDR').text
except:
    print "没有住所信息"
#经营范围
result['scope']=driver.find_element_by_id('FARE_SCOPE').text

#print ('经营异常名录列入公告').decode('utf-8').encode('gbk')
#print result

try:
    gudongcont = driver.find_element_by_xpath('//*[@id="gdczList"]').text
    print gudongcont
except:
    print "没有股东信息"


try:
    choucha=driver.find_element_by_xpath('//*[@id="ccjcList"]').text
    print choucha
except:
    print '没有抽查信息'



    #试下能不能定位到元素2，结果是可以的
try:
    driver.find_element_by_xpath('//*[@id="gdczList_pt"]/div/a[1]').text
    print "能捕获换页标签"
except:
    print "没有换页标签，页码只到当前一页"


#向字典里加入数据
def addWord(dict,key,value):
  dict.setdefault(key, [ ]).append(value)#存在就在基础上加入列表，不存在就新建个字典key

#把result用pandas处理
addWord(result,'A',range(1))
d_result = df.DataFrame(result)

#打印出股东信息，抽查结果，基本信息

print d_result

#将基本信息导出
d_result.to_excel('compan1_info.xlsx')#倒出的文件名不可以是已经存在的，否则会报permission error
#将字典按中文输出
# df = pandas.DataFrame(result)
# print df.to_excel('Cinfo.xlsx')
#加入cookies
#get the session cookie
cookie = [item["name"] + ":" + item["value"] for item in driver.get_cookies()]
#print cookie

cookiestr = ','.join(item for item in cookie)
print cookiestr

# homeurl = driver.current_url
# print 'homeurl: %s' % homeurl
#cookie每请求一次，改变一次
# driver.add_cookie()
# print '%%%using the urllib2 !!'
#homeurl = driver.current_url
#print 'homeurl: %s' % homeurl
#有重新用原来的方式打开，ip仍然被封了，还要重新设置ip代理。才能打开网页。urllib2不能抓到动态网页。拜拜
# headers = {'cookie':cookiestr}
# req = urllib2.Request(homeurl, headers = headers,)
# #try:
# response = urllib2.urlopen(req)
# text = response.read()
   # print '###get home page html success!!'
#except:
   # print '### get home page html error!!'

#股东下一页....待编辑,还要加入判断有没有下一页
try:
    driver.find_element_by_xpath('//*[@id="gdczList_pt"]/div/a[1]').clik()
    print 'click succed!'
    gudongcont1 = driver.find_element_by_xpath('//*[@id="gdczList"]').text
except:
    print 'click failed!'
#使用js试下能不能行，成功。！！！
try:
    js = 'document.getElementsByClassName("next")[0].click();'
    driver.execute_script(js)
    print 'js succed!'
    time.sleep(3)
    gudongcont2 = driver.find_element_by_xpath('//*[@id="gdczList"]').text

    print "我打印的是股东2："
    print gudongcont2
except:
    print"js failed!"
#股东出资详情页面
try:
    driver.find_element_by_xpath('//*[@id="gdczList"]/tbody/tr[1]/td[6]/a').click()
except:
    print "进入详情页失败"


time.sleep(3)

try:
    for num in range(1000):
        driver.switch_to.frame("'layui-layer-iframe'+num")
except:
    print "获取详情页失败"

print driver.page_source



driver.close()

