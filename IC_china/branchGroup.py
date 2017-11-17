#-*- coding:utf-8 -*-

from selenium import webdriver
import csv
import time
import codecs
import re
import sys
from selenium.webdriver.common.action_chains import ActionChains

reload(sys)
sys.setdefaultencoding('utf-8')

#代理
# PROXY='117.66.82.37:8118'
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' %PROXY)
# url = 'http://www.gsxt.gov.cn/%7BBbZbEVENjiufwCaVHhxU5D0HzJXw-3X6kU_fIGnL_DOh0OjaUeTxf2_ksBLfg47l8yONiehTv6iXjaSIdt50cGmDCY7e08jd-mJaEp3mOWlB9TTcmKOp7FKUjF_h46HH-1510819280826%7D'
url = 'http://www.gsxt.gov.cn/%7BBbZbEVENjiufwCaVHhxU5D0HzJXw-3X6kU_fIGnL_DOh0OjaUeTxf2_ksBLfg47lvctkB_6r0kBnRakMjmuJXKVNFeC7kuKaOXtC5hBG6ZyJ-gkK-8N4AWHS131jCD42rGhXcadEB41RaLXWIw6fXQ-1510816975425%7D'
driver = webdriver.Chrome()
#全屏
# driver.maximize_window()
# driver.set_window_size(1280,800)  # 分辨率 1280*800
time.sleep(1)
driver.get(url)
if driver.current_url=='http://www.gsxt.gov.cn/index/invalidLink':
    pass
else:
    #留出页面加载时间
    time.sleep(5)
    #窗口向下滚动
    driver.execute_script("window.scrollBy(0,2000)")
    time.sleep(3)
    # driver.execute_script("window.scrollBy(0,500)")
    # time.sleep(3)
    driver.execute_script("window.scrollBy(100,0)")
def branchGroup():
    total=[]
    social_code = driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
    name=['branch_place','branch_social_unique_code','branch_register_oran','social_unique_code']
     #得到分支机构总数
    try:
        branch_num = driver.find_element_by_xpath('//*[@id="branchCount"]').text

        branch_num= re.findall(r'\d+',branch_num)[0]
        print "有多少个分支机构",branch_num
    except:
        branch_num=0


    #查看有没有更多分支机构的连接页面：
    try:
        more=driver.find_element_by_xpath('//*[@id="branchForAll"]/span/a[2]')
    except:
        more = None

    if more:
        # ActionChains(driver).move_to_element(more).click(more).perform()
        driver.find_element_by_xpath('//*[@id="branchForAll"]/span/a[2]').click()
        time.sleep(10)
        #点击下拉加载的内容,尝试四：WebDriver 的 click() 对隐藏的元素是否生效。试过，结论是：不可以。尝试五：Javascript 的 click() 对隐藏的元素是否生效。试过，结论是：可以。这样，问题就迎刃而解了，可以跳过鼠标悬停 project 这个步骤，直接点击 datasource 就行了
        #切换到最后一个window__handler里
        driver.switch_to_window(driver.window_handles[-1])
        while True:
            #加载完了以后‘加载更多在页面不可见，但是html里还有，这就导致了click失败’
            driver.execute_script("window.scrollBy(0,100)")
            driver.execute_script("window.scrollBy(0,500)")
            try:
                # jiazhai = driver.find_element_by_css_selector('#more > a:nth-child(2) > span:nth-child(1)')
                jiazhai = driver.find_element_by_css_selector('#more > a:nth-child(2) > span:nth-child(1)')
                print jiazhai
            except:
                jiazhai = None
            if jiazhai:
                try:
                    # ActionChains(driver).move_to_element(jiazhai).click(jiazhai).perform()
                    driver.find_element_by_css_selector('#more > a:nth-child(2) > span:nth-child(1)').click()
                    time.sleep(5)
                except:
                    break
            else:
                break

    for i in range(int(branch_num)):
        result={'branch_place':'null','branch_social_unique_code':'null','branch_register_oran':'null','social_unique_code':'null'}

        if branch_num==0:
            break
        #取得办事处
        try:
            result[name[0]] =driver.find_element_by_xpath('//*[@id="branchGroupForAll"]/li[%d]/a/div'%(i+1)).text
        except:
            print "over"
            break
        #取得分支机构社会统一代码，//*[@id="branchGroupForAll"]/li/a/span/span/img，还有以图片的形式给数据的。此处没有处理
        try:
            result[name[1]] =driver.find_element_by_xpath('//*[@id="branchGroupForAll"]/li[%d]/a/span/span'%(i+1)).text
        except:
           result[name[1]] = None
        #取得分支机构登记机关
        try:
            result[name[2]] =driver.find_element_by_xpath('//*[@id="branchGroupForAll"]/li[%d]/a/span/div/span'%(i+1)).text
        except:
            result[name[2]] = None

        result[name[3]]=social_code
        # print result[name[1]]
        total.append(result)


    #判断句柄是不是在主页，不是就关掉当前的句柄，切换到第一句柄
    if driver.window_handles[-1]!=driver.window_handles[0]:
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    else:
        pass
    with codecs.open('bg.csv','a+','utf-8') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=name)
        for i in range(len(total)):
            writer.writerow(total[i])
        print total
    return total

branchGroup()
# driver.get('http://www.gsxt.gov.cn/%7BBbZbEVENjiufwCaVHhxU5JMehYfg8e5cA23BZIK3Wpuy3X4W7rbNHTEQn03NBQnZgjATytQdgRCxmW3i_hBt5qr2KluJeVtV_w2FqkeO7F3oq0c2TEswsT4-VrIyWYEt9vt1xFiUzrSmrc--dwENcA-1510812445861%7D')
# time.sleep(10)
# a=driver.find_element_by_css_selector('#more > a:nth-child(2) > span:nth-child(1)')
# print a
# ActionChains(driver).move_to_element(a).click(a).perform()
# # driver.find_element_by_css_selector('#more > a:nth-child(2) > span:nth-child(1)').click()
# time.sleep(5)
driver.close()