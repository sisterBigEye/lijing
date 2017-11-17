#-*- coding:utf-8 -*-
import requests
import urllib2
import urllib
import lxml.html
import pprint
from selenium import  webdriver
from PIL import Image
import time
import pytesseract
# def parse_form(html):
#     tree = lxml.html.fromstring(html)
#     data={}
#     for e in tree.cssselect('form input'):
#         if e.get('name'):
#             data[e.get('name')] = e.get('value')
#     return data
#
# # html = requests.get('http://www.renren.com/').content
# html = urllib2.urlopen('http://www.renren.com/').read()
# form = parse_form(html)
# pprint.pprint(form)

# url='http://www.renren.com/'
# icodeurl='http://icode.renren.com/getcode.do?t=web_login&rnd=0.045085975406540246'
# email='376700233@qq.com'
# password='376700233lj'
# icode=''
# requests.post(url,data=data)
# data = parse_form(html)
# data={}
# data['email']='376700233'
# data['password']='lj376700233'
# encoded_data = urllib.urlencode(data)
# request=urllib2.Request(url,encoded_data)
# response = urllib2.urlopen(request)
# print response.geturl()



driver = webdriver.PhantomJS()
# url='http://wenshu.court.gov.cn/waf_verify.htm'
url ='http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html'
# driver.set_window_size(1200,800)
driver.get(url)
time.sleep(30)
cookies = driver.get_cookies()
p=driver.find_element_by_xpath('//*[@id="Login"]/div/div').text
print p


def vertifcode():
    driver.save_screenshot('screenshot.png')

    # #
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













