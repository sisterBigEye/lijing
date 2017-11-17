#-*- coding:utf-8 -*-
from  selenium import webdriver
import re

import pandas

url='http://www.cbrc.gov.cn/chinese/home/docView/DF5E4623B34C4B2793478F03E118C10D.html'
driver=webdriver.Chrome()
result={}
data=[]
driver.get(url)
name=[u'文书标题',u'公示日期',u'详情url',u'决定书文号',u'被处罚个人姓名',u'被处罚个人单位',u'被处罚机构名称',u'机构负责人',u'案由',u'处罚依据',u'处罚内容',u'做出处罚机构的名称',u'处罚日期']
result[name[2]]=url
try:
    header=driver.find_element_by_css_selector('#docTitle > div:nth-child(3)').text
    result[name[1]]=re.findall(r'(\d+\-\d+\-\d+|\d+\/\d+\/\d+)',header)[0]
except:
    result[name[1]]=''
try:
    result[name[3]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)').text
except:
    result[name[3]]='null42'
try:
    result[name[4]]=driver.find_element_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3)').text
except:
    result[name[4]]='null42'
result[name[5]]='null42'
try:
    result[name[6]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(3)')[0].text
except:
    result[name[6]]='null42'
for i in range(7,len(name)):
    try:
        result[name[i]]=driver.find_elements_by_css_selector('.MsoNormalTable > tbody:nth-child(1) > tr:nth-child(%d) > td:nth-child(2)'%i)[0].text
    except:
        result[name[i]]='null42'

result[name[0]]=result[name[11]]+u'行政处罚信息公开表'
data.append(result)

pd=pandas.DataFrame(data)
pd.to_excel('333.xlsx')

driver.close()
