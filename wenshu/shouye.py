#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import requests as req
import pandas
import re

reload(sys)
sys.setdefaultencoding('utf-8')


driver = webdriver.Chrome()
# driver = webdriver.PhantomJS()
print "请输入您想搜索的案件名："
keyword=raw_input().decode('utf-8')
url = 'http://wenshu.court.gov.cn/'

driver.get(url)
driver.implicitly_wait(30)

try:
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="head_maxsearch_btn"]'))).click()
except Exception as msg:
    print(u"异常原因%s"%msg)

time.sleep(300)
driver.get(url)
    #给图片名称加个时间戳
    # nowTime1 = time.strftime("%Y%m%d.%H.%S")
    # h = driver.get_screenshot_as_file('yesgu%s.jpg'%nowTime1)
    # print(u'截图结果： %s' %h)

# driver.find_element_by_xpath('//*[@id="head_maxsearch_btn"]').click()
# time.sleep(1)

driver.find_element_by_xpath('//*[@id="adsearch_AJMC"]').send_keys(keyword)
# time.sleep(3)
driver.execute_script('window.scrollBy(0,100)')
driver.find_element_by_xpath('//*[@id="list_btnmaxsearch"]').click()

#获取当前url
curpage_url = driver.current_url

print curpage_url
res1=req.get(curpage_url)
#获得cookies
cookies=req.utils.dict_from_cookiejar(res1.cookies)
print cookies
#request获取不到内容
# r=req.post(curpage_url,cookies=cookies)
# print r.text
#搜索得到的文书总数,re.findall返回的是list
try:
    b=WebDriverWait(driver,50).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'dataItem')))
    print 'b one is ',b[1]
except Exception as msg:
    print(u"异常原因%s"%msg)

driver.execute_script('window.scrollBy(100,0)')
#总条数


n=int((re.findall('\d+',driver.find_element_by_xpath('//*[@id="sort"]/div[4]').text))[0])

driver.execute_script('window.scrollBy(0,3000)')
driver.execute_script('window.scrollBy(0,5000)')

# time.sleep(5)
#选择最多显示20条
menuS = driver.find_element_by_xpath('//*[@id="12_button"]')
hidden_submenu = driver.find_element_by_xpath('//*[@id="12_input_20"]')

ActionChains(driver).move_to_element(menuS).click(menuS).move_to_element(hidden_submenu).click(hidden_submenu).perform()
# time.sleep(50)

driver.execute_script('window.scrollBy(0,-2000)')
countdata=[]

#算出总页面数
if n%20==0:
    n1=n/20
else:
    n1=n/20+1
for i in range(n1):
    try:
        a=WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'dataItem')))
        print 'a is ',len(a)
    except:
        break
    driver.execute_script('window.scrollBy(200,0)')

    #选择批量下载
    #在第一页选中批量，以后的下一页也是选中的，需要再次模拟,先点击取消，再点击选中，然后下载
    try:
        bar = driver.find_element_by_xpath('//*[@id="ckall"]')
        batchdown = driver.find_element_by_xpath('//*[@id="operate"]/div[2]/span')
    except:
        print"被验证码打断了"
        break
    if i==0:
        ActionChains(driver).move_to_element(bar).click(bar).move_to_element(batchdown).click(batchdown).perform()
        print('do')
    else:
        ActionChains(driver).move_to_element(bar).click(bar).click(bar).move_to_element(batchdown).click(batchdown).perform()

    for j in range(1,21):
        result={}

        driver.execute_script('window.scrollBy(0,500)')
        try:
            #获取信息
            result['biao']=driver.find_element_by_xpath('//*[@id="resultList"]/div[%d]/div[1]'%j).text
        except:
            break
        result['title'] = driver.find_element_by_xpath('//*[@id="resultList"]/div[%d]/table/tbody/tr[1]/td/div'%j).text
        courtdata =driver.find_element_by_xpath('//*[@id="resultList"]/div[%d]/table/tbody/tr[2]/td/div'%j).text
        result['court'] = courtdata.split('    ')[0]
        result['number'] = courtdata.split('    ')[1]
        result['date'] = courtdata.split('    ')[2]
        result['mainreason']=driver.find_element_by_xpath('//*[@id="resultList"]/div[%d]/table/tbody/tr[4]/td'%j).text
        countdata.append(result)

    #点击下一页
    driver.execute_script('window.scrollBy(3000,0)')
    try:
        if re.search(ur'下一页',driver.find_element_by_xpath('//*[@id="pageNumber"]/a[7]').text):
            driver.find_element_by_xpath('//*[@id="pageNumber"]/a[7]').click()
    except:
        try:
            if re.search(ur'下一页',driver.find_element_by_xpath('//*[@id="pageNumber"]/a[6]').text):
                driver.find_element_by_xpath('//*[@id="pageNumber"]/a[6]').click()
        except:
            try:
                if re.search(ur'下一页',driver.find_element_by_xpath('//*[@id="pageNumber"]/a[5]').text):
                    driver.find_element_by_xpath('//*[@id="pageNumber"]/a[5]').click()
            except:
                try:
                    if re.search(ur'下一页',driver.find_element_by_xpath('//*[@id="pageNumber"]/a[4]').text):
                        driver.find_element_by_xpath('//*[@id="pageNumber"]/a[4]').click()
                except:
                    try:
                        if re.search(ur'下一页',driver.find_element_by_xpath('//*[@id="pageNumber"]/a[3]').text):
                            driver.find_element_by_xpath('//*[@id="pageNumber"]/a[3]').click()
                    except:
                        try:
                            if re.search(ur'下一页',driver.find_element_by_xpath('//*[@id="pageNumber"]/span[2]').text):
                                break
                        except:
                            try:
                                if re.search(ur'下一页',driver.find_element_by_xpath('//*[@id="pageNumber"]/span[3]').text):
                                    break
                            except Exception as msg:
                                print(u"异常原因%s"%msg)
                                #给图片名称加个时间戳
                                nowTime = time.strftime("%Y%m%d.%H.%S")
                                break
                                # t = driver.get_screenshot_as_file('%s.jpg'%nowTime)
                                # print(u'截图结果： %s' %t)

    driver.execute_script('window.scrollBy(0,-5000)')


pd=pandas.DataFrame(countdata)
pd.to_excel('yili.xlsx')

