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
import Image
import pytesseract

reload(sys)
sys.setdefaultencoding('utf-8')

# 识别验证码1的函数
def vertifcode():
    driver.save_screenshot('screenshot.png')
    # #获取指定元素位置
    element = driver.find_element_by_xpath('//*[@id="trValidateCode"]/td[2]/img')
    left = int(element.location['x'])
    top = int(element.location['y'])
    right = int(element.location['x'] +element.size['width'])
    bottom = int(element.location['y']+element.size['height'])


    #通过Image处理图像
    im = Image.open('screenshot.png')
    im = im.crop((left,top,right,bottom))
    im.save('code.png')

    img= Image.open('code.png')
    return pytesseract.image_to_string(img)


driver = webdriver.Chrome()
# driver = webdriver.PhantomJS()
verturl='http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html'
url = 'http://wenshu.court.gov.cn/'
def detailye(url):
    countdata=[]
    i=1
    driver.get(url)
    driver.implicitly_wait(30)
    #刚进入网页时，网页是否要输入验证码
    while i:
        i=i-1
        if driver.current_url==verturl and driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
            driver.find_element_by_xpath('//*[@id="txtValidateCode"]').send_keys(vertifcode())
            driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
        elif driver.current_url==verturl and not driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
            break
        else:
            #刚进入网页时，网页是可以访问
            if driver.current_url==url and not re.search(ur'无法访问此网页',driver.find_element_by_xpath('//*[@id="main-message"]/h1').text):
                while True:
                    #等search框出现并点击，没有就中断
                    try:
                        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="head_maxsearch_btn"]'))).click()
                    except Exception as msg:
                        print(u"异常原因%s"%msg)
                        #给图片名称加个时间戳
                        # nowTime1 = time.strftime("%Y%m%d.%H.%S")
                        # h = driver.get_screenshot_as_file('yesgu%s.jpg'%nowTime1)
                        # print(u'截图结果： %s' %h)
                        break
                    # driver.find_element_by_xpath('//*[@id="head_maxsearch_btn"]').click()
                    # time.sleep(1)
                    #找到案件输入，没有就中断
                    try:
                        driver.find_element_by_xpath('//*[@id="adsearch_AJMC"]').send_keys(u'伊利')
                    except:
                        break
                    # time.sleep(3)
                    driver.execute_script('window.scrollBy(0,100)')
                    try:
                        driver.find_element_by_xpath('//*[@id="list_btnmaxsearch"]').click()
                    except:
                        break
                    #获取当前url，看看是否要输入验证码
                    if driver.current_url==verturl and driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                        driver.find_element_by_xpath('//*[@id="txtValidateCode"]').send_keys(vertifcode())
                        driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
                    elif driver.current_url==verturl and not driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                        break
                    else:
                        pass
                    #搜索得到的文书总数,re.findall返回的是list
                    try:
                        WebDriverWait(driver,50).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'dataItem')))
                    except Exception as msg:
                        print(u"异常原因%s"%msg)
                        break

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
                    if driver.current_url==verturl and driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                        driver.find_element_by_xpath('//*[@id="txtValidateCode"]').send_keys(vertifcode())
                        driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
                    elif driver.current_url==verturl and not driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                        break
                    else:
                        pass
                    driver.execute_script('window.scrollBy(0,-2000)')


                    #算出总页面数
                    if n%20==0:
                        n1=n/20
                    else:
                        n1=n/20+1
                    for i in range(n1):
                        try:
                            WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'dataItem')))
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
                        if driver.current_url==verturl and driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                            driver.find_element_by_xpath('//*[@id="txtValidateCode"]').send_keys(vertifcode())
                            driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
                        elif driver.current_url==verturl and not driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                            break
                        else:
                            pass
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
                        if driver.current_url==verturl and driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                            driver.find_element_by_xpath('//*[@id="txtValidateCode"]').send_keys(vertifcode())
                            driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
                        elif driver.current_url==verturl and not driver.find_element_by_xpath('//*[@id="Login"]/div/div'):
                            break
                        else:
                            pass
                        driver.execute_script('window.scrollBy(0,-5000)')
                # pd=pandas.DataFrame(countdata)
                # pd.to_excel('yili.xlsx')
            else:
                pass

    return countdata


