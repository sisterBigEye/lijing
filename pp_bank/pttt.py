#-*- coding:utf-8 -*-
import csv
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')




with codecs.open('bank_punish.csv','a+','utf-8') as csvfile:
    name=[u'文书标题',u'公示日期',u'详情url',u'决定书文号',u'被处罚个人姓名',u'被处罚个人单位',u'被处罚机构名称',u'机构负责人',u'案由',u'处罚依据',u'处罚内容',u'做出处罚机构的名称',u'处罚日期']
    writer =csv.DictWriter(csvfile,fieldnames=name)
    csvfile.seek(0)
    writer.writeheader()
