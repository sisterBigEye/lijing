#-*- coding: utf-8 -*-

from selenium import webdriver
import time

url='http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=78AB4DDC058110BDAA3B82E7C2990A07&id=CDE1AAF36B38E29EFB8A431642FF7A12&seqId=87A6149475C405CD57034644DD2BD82C&activeTabId='

driver=webdriver.Chrome()
driver.get(url)
time.sleep(3)
#股东出资详情页面,第一个股东
try:
    driver.find_element_by_xpath('//*[@id="gdczList"]/tbody/tr[1]/td[6]/a').click()
except:
    print "进入详情页失败"
time.sleep(3)

#每次重新打开网址，layer是从1开始的。和自己分析页面时点击后看到的可能不太一样，这个数字和第几次点击有关系
text1=driver.find_element_by_xpath('//*[@id="layui-layer1"]')
#测试是否成功跳转到iframe里
text2 = text1.find_element_by_tag_name("iframe").get_attribute("src")
print text1
print text2
#弹出框的iframe
#找到iframe并跳转进去，然后获取元素
text = text1.find_element_by_tag_name('iframe')
driver.switch_to.frame(text)
#股东认缴额
invest=driver.find_element_by_xpath('//*[@id="SHOULD_CAPI"]').text
print invest
driver.switch_to.default_content()





#查看https://www.baidu.com/link?url=73IPFRpqNca0JZLDSXYog_j3F6PeT4LjbD_pPcxpgZWcBz6ToO1r6sGNvoAMtOcamt1PhtzS6s8juWRSvMpKn_&wd=&eqid=e1d6648800007fa50000000459917322
#
# try:
#     try:
#         for num in range(1,100):
#             lay =('layui-layer-iframe'+str(num))
#             print lay
#             if driver.switch_to.frame('lay'):
#                 time.sleep(3)
#                 xiangzi=driver.find_element_by_xpath('//*[@id="layui-layer1"]')
#             else:
#                 pass
#     except:
#         print "找不到"
#
#
# except:
#     print "获取详情页失败"
#
#
#
#
# driver.close()

#数字和字符串连接
# for num in range(10):
#     print(('layui-layer-iframe')+str(num))