#-*- coding:utf-8 -*-
import pandas
import requests
import re
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import time

reload(sys)
sys.setdefaultencoding('utf-8')

#手动输入搜索关键字
print"请输入你想搜索的内容关键字吧："
inn = raw_input().decode('utf-8')

print "how many news you want:"
howmany =raw_input()


def page_num(n):
    #判断输入是否是整数
    para=[]
    #判断用户键盘输入是否都是数字
    while not n.isdigit():
        print("输入有误，请重新输入：")
        n =raw_input()
    n=int(n)
    if n>20 and n/20==0:
        yeshu=n/20
        para.append(yeshu)
    elif n<20:
        yeshu=1
        para.append(yeshu)
    else:
        yeshu=n/20+1
        para.append(yeshu)
    para.append(n)
    return para



url = 'http://news.baidu.com/'
# driver = webdriver.PhantomJS()
driver = webdriver.Chrome()

# inn=u'洗洁精检查'
driver.get(url)
driver.find_element_by_xpath('//*[@id="ww"]').send_keys(inn)
driver.find_element_by_xpath('//*[@id="sugarea"]/span[2]/input').click()
time.sleep(3)
#request访问行不通
# print("请输入关键词：")
# pythonin=raw_input()
#
# res=requests.get(url,params={'word':pythonin,'tn':'news','from':'news','cl':2,'rn':20,'ct':1})
# print res.status_code
# print res.url
# print requests.get(res.url).text
def getnewslist(param):

    tit=[]
    alink=[]
    cm=[]
    comes=[]
    tdate=[]
    st=[]
    subcontent=[]
    for j in range(param[0]):
        current_url = driver.current_url
        print current_url
        res=requests.get(current_url).text

        soup = BeautifulSoup(res)
        # countnum = int(re.findall(r'\d+',soup.select('.nums')[0])[0])
        #搜索的结果数量,还需要处理,600,000转化，整数int()
        if j==0:
            countnum =soup.select('.nums')[0]
            print str(countnum)
            # cn=int(re.findall(r'\d+,\d+,\d+,\d+|\d+,\d,\d+|\d+,\d', str(countnum))[0].strip(','))
            cn=re.findall(r'\d+,\d+,\d+,\d+|\d+,\d+,\d+|\d+,\d+|\d+', str(countnum))[0]
            print int(cn.replace(',',''))

        #标题成功获取
        try:
            title=soup.select('.c-title')
        except:
            break
        for tl in title:
            tit.append(tl.text)


        #链接获取成功
        linkurl = soup.select('.c-title a')
        for lk in linkurl:
            alink.append(lk['href'])


        #成功获取来源，还需要处理时间，把来源与时间分开
        comefrom=soup.select('.c-author')
        for cf in comefrom:
            # print cf.text
            cm.append(cf.text)

        #取去源网站名
        for i in range(len(cm)):
            #看下出取出的信息是否正确，split的串是unicode类型，从cm的结果中，取出试出来的
            # print cm[i].split(u'\xa0')[0]
            comes.append(cm[i].split(u'\xa0')[0])


        #取出时间
        for i in range(len(cm)):
            # tm=cm[i].lstrip(comes[i])
            # print tm
            if re.search(ur'前',cm[i]):
                tdate.append(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            else:
                #去掉后面的具体时间
                # print re.findall(ur'\d+年\d+月\d+日',cm[i])[0]
                tdate.append(re.findall(ur'\d+年\d+月\d+日',cm[i])[0])
                # tdate.append(tm)




        # pub_time=datetime.date
        #概要内容
        subtext=soup.select('.result')
        for s in subtext:
            st.append( s.text)

         #.lstrip(tit[i]).lstrip(cm[i])做取出多余字符串处理
        for i in range(len(st)):
            subcontent.append(st[i].lstrip(tit[i]).lstrip(cm[i]))


        #测试split应该用什么而打印的
        # print cm

        #获取的需求信息

        # print subcontent
        # print comes
        # print tdate
        # print tit
        # print alink
        # print len(tit)
        # try:
        #     driver.find_element_by_xpath('//*[@id="page"]/a[%d]'%(i+1)).click()
        # except:
        #     break
        driver.execute_script('window.scrollBy(0,3000)')
        driver.execute_script("window.scrollBy(0,5000)")
        time.sleep(1)
        if j==0:
            driver.find_element_by_xpath('//*[@id="page"]/a[1]/span[2]').click()
        else:
            if j+2<=7:
                try:
                    driver.find_element_by_xpath('//*[@id="page"]/a[%d]/span[2] '%(j+2)).click()
                except:
                    break
            else:
                if j>=10:
                    try:
                        #用下一页来做超过10页的页码点击
                        driver.find_element_by_xpath('//*[@id="page"]/a[11]').click()
                    except:
                        break
                elif j==9:
                    try:
                         #用下一页来做超过9页的页码点击
                        driver.find_element_by_xpath('//*[@id="page"]/a[10]').click()
                    except:
                        break
                elif j==8:
                    try:
                        driver.find_element_by_xpath('//*[@id="page"]/a[9]').click()
                    except:
                        break
                # elif j==7:
                #     try:
                #         driver.find_element_by_xpath('//*[@id="page"]/a[8]').click()
                #     except:
                #         break

        time.sleep(1)
    #取得要的新闻总数，实际得到的数量可能会比用户要的多，截取一下
    total = zip(tit,tdate,alink,comes,subcontent)[:param[1]]
    print len(total)
    if len(total)< param[1]:
        print '您输入的新闻条数大于总新闻条数!'
    return total

da = getnewslist(page_num(howmany))

pd =pandas.DataFrame(da,columns=['title','pub_date','url','come','abstract'])
pd.to_csv('news.csv')
