#-*- coding: utf-8 -*-
import urllib2
import time

#url = 'http://www.jsgsj.gov.cn:58888/province/notice/InformationNotice.jsp'
# postData = {
#     'type':1,
#     'all':all,
#     'pageSize':100,
#     'curPage':1,
# }
url = 'http://www.jsgsj.gov.cn:58888/province/NoticeServlet.json?ExceptionNoteList=true'
request =urllib2.Request(url)
request.add_header( 'User-Agent','Mozilla/5.0')
request.add_data('type:1, all:all,pageSize:100,curPage:1')

response = urllib2.urlopen(request)
time.sleep(3)
print response.read()
