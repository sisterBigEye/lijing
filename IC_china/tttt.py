#-*- coding:utf-8 -*-
# from PIL import Image
# import pytesseract
#
# image=Image.open("capt.png")    #打开验证码图片
# # image.load()        #加载一下图片，防止报错，此处可省略
# # image.show() #调用show来展示图片，调试用，可省略
#
# vcode=pytesseract.image_to_string(image)
# print vcode
#-*- coding:utf-8 -*-
from io import BytesIO
import lxml.html
from PIL import Image
from selenium import webdriver
import time
import pytesseract
# from pytesseract import image_to_string
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait

url = 'http://www.gsxt.gov.cn/%7BasyxP4MFJFgm3OY7yHkTtbQOmlckLcqNH0BTPuLEGOtbTtXBbkfQsNsUFLJDQyoImvXRKCI8XXlIVxdC1VjpWllVmBY5FTzhKhSeQmdJVA6Z3YbcR-qiaIS13WyIhNkR-1509504897447%7D'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
driver.execute_script("window.scrollBy(0,3000)")
time.sleep(1)
driver.execute_script("window.scrollBy(0,5000)")
time.sleep(1)
html = driver.page_source


def get_captcha(html):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('html body div.container div.container1 div.result div.page div.content div#content1.content-i div#wrap-keyperson.wrap div#keyPerson.keyPerson div#personInfo.clearfix ul.people-list li a div.people-list-position span img')[0].get('src')
    img_data =img_data.partition(',')[-1]
    binary_img_data = img_data.decode('base64')
    file_like = BytesIO(binary_img_data)
    img = Image.open(file_like)
    img.save('capt.png')
    return img

img = get_captcha(html)
pytesseract.image_to_string(img)

