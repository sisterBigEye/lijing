#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd




#向字典里加入数据
def addWord(dict,key,value):
  dict.setdefault(key, [ ]).append(value)#存在就在基础上加入列表，不存在就新建个字典key



d = {"hello":[3]}
#d = {}
addWord(d,"hello",3)
addWord(d,"hello",56)
addWord(d,"nihao",24)
print d
#设计一个字典
d_data = {'A':1,'B':pd.Timestamp('20170220'),'C':range(4),'D':np.arange(4)}
#给单个字典加一个可以表示范围的索引，这里用'A':range(1)
dic = {'end_open': u'2029\u5e7405\u670810\u65e5', 'law_man': u'\u9648\u5b87\u7ea2', 'title': u'\u4e2d\u8f6f\u56fd\u9645\u8d44\u6e90\u4fe1\u606f\u6280\u672f\uff08\u65e0\u9521\uff09\u6709\u9650\u516c\u53f8', 'money': u'300\u4e07\u7f8e\u5143', 'open_place': u'\u65e0\u9521\u65b0\u533a\u6c5f\u82cf\u8f6f\u4ef6\u5916\u5305\u56ed\u5904\u5b50\u5ea7B\u680b4-6\u5c42', 'kind': u'\u6709\u9650\u8d23\u4efb\u516c\u53f8(\u53f0\u6e2f\u6fb3\u6cd5\u4eba\u72ec\u8d44)', 'registerID': u'913202146891550956', 'start_open': u'2009\u5e7405\u670811\u65e5', 'reg_place': u'\u65e0\u9521\u5e02\u65b0\u5434\u533a\u5e02\u573a\u76d1\u7763\u7ba1\u7406\u5c40', 'company_name': u'\u4e2d\u8f6f\u56fd\u9645\u8d44\u6e90\u4fe1\u606f\u6280\u672f\uff08\u65e0\u9521\uff09\u6709\u9650\u516c\u53f8', 'es_date': u'2009\u5e7405\u670811\u65e5', 'scope': u'\u8ba1\u7b97\u673a\u8f6f\u4ef6\u7684\u7814\u53d1\uff1b\u63d0\u4f9b\u6280\u672f\u670d\u52a1\u548c\u54a8\u8be2\u670d\u52a1\uff1b\u6570\u636e\u5904\u7406\uff1b\u8ba1\u7b97\u673a\u7cfb\u7edf\u96c6\u6210\uff1b\u81ea\u8425\u548c\u4ee3\u7406\u5404\u7c7b\u5546\u54c1\u548c\u6280\u672f\u7684\u8fdb\u51fa\u53e3\u4e1a\u52a1\uff08\u56fd\u5bb6\u9650\u5b9a\u4f01\u4e1a\u7ecf\u8425\u548c\u7981\u6b62\u8fdb\u51fa\u53e3\u7684\u5546\u54c1\u548c\u6280\u672f\u9664\u5916\uff0c\u4e0d\u542b\u5206\u9500\u53ca\u5176\u5b83\u56fd\u5bb6\u7981\u6b62\u3001\u9650\u5236\u7c7b\u9879\u76ee\uff09\u3002\uff08\u4f9d\u6cd5\u987b\u7ecf\u6279\u51c6\u7684\u9879\u76ee\uff0c\u7ecf\u76f8\u5173\u90e8\u95e8\u6279\u51c6\u540e\u65b9\u53ef\u5f00\u5c55\u7ecf\u8425\u6d3b\u52a8\uff09', 'pemi_date': u'2016\u5e7403\u670830\u65e5'}

addWord(dic,'A',range(1))
print dic
d={'1':'a','2':'b','c':'232','3':range(3)}
print d_data

#使用字典生成一个DataFrame
df_data = pd.DataFrame(d_data)
df_dic = pd.DataFrame(dic)
d_df=pd.DataFrame(d)
print df_data
print d_df
print df_dic

df_dic.to_excel('d_df.xlsx')
#DataFrame中每一列的类型
print df_data
#打印A列
print df_data.A
#打印B列
print df_data.B
#B列的类型
print type(df_data.B)