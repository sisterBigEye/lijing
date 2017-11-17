#-*- coding:utf-8 -*-
import time
import re
# import csv
# import codecs
# # a=[{1,2,3},{4,5,6}]
# b=[{'一':'a','二':'b','三':'c'},{'一':'e','二':'f','三':'g'}]
# c=[{'一':'1b','二':'bb','三':'cf'},{'一':'hh','二':'d','三':'zz'}]
#
# list=[]
#
# # list.extend(a)
# list.extend(b)
# list.extend(c)
#
# print list
#
# with open('dicw.csv','a+')  as csvfile:
#     #fieldnames =[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
#     fieldnames=['一','二','三']
#     writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
#     writer.writeheader()
#     for i in range(len(list)):
#         writer.writerow(list[i])
#
# a=['一','二','三']
# b={}
# for i in range(len(a)):
#     b[a[i]]='asjdl'+'%d'%i
#
# print b
#
# with open('dicw1.csv','a+')  as csvfile1:
#     #fieldnames =[u'行政处罚决定书文号',u'处罚个人姓名',u'处罚个人单位',u'处罚单位名称',u'处罚单位法定代表人（主要负责人）姓名',u'主要违法违规事实（案由）',u'行政处罚依据',u'行政处罚决定',u'作出处罚决定的机关名称',u'作出处罚决定的日期']
#     fieldnames1=['一','二','三']
#     writer1=csv.DictWriter(csvfile1,fieldnames=fieldnames1)
#     writer1.writeheader()
#     writer1.writerow(b)
# def f(a):
#     c=a
#     return c
#
# print f(2)

a=[]
if 2:
    a.append(2)

print a
b={'a':"hah",'b':'ss'}
print b['a']+u'gg'


#时间转换
str='2017.6.12'
s= re.findall(r'\d+',str)
time1=''
for i in range(len(s)):
    time1=time1+re.findall(r'\d+',str)[i]+'-'
print time1.rstrip('-')

def timesf(str):
    s=re.findall(r'\d+',str)
    time1=''
    for i in range(len(s)):
        time1=time1+s[i]+'-'
        str=time1.rstrip('-')