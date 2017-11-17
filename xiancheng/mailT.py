#-*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

my_sender='376700233@qq.com'
my_pass='yvxdtvaxespebige'
my_user = '376700233@qq.com'


def mail():
    ret = True
    try:
        #简单文字实例
        # msg=MIMEText('THIS is content.....thing...','plain','utf-8')
        # msg['From'] = formataddr(['FromRunoob',my_sender])
        # msg['To'] = formataddr(["kinglee",my_sender])
        # msg['Subject'] = '李静的测试邮件'
        #创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header("菜鸟教程",'utf-8')
        message['To'] = Header('测试','utf-8')
        subject = 'Python SMTP邮件测试'
        message['Subject'] = Header(subject,'utf-8')

        #邮件正文内容
        message.attach(MIMEText('this is python mail sending.....','plain','utf-8'))

        #构造附件1，传送当前目录下的test.txt文件
        att1 = MIMEText(open('foo.csv','rb').read(),'base64()','utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        #filename可以任意写，写什么名字，邮件显示什么名字
        att1['Content-Disposition'] = 'attachement;filename=foo.csv'
        message.attach(att1)


        server=smtplib.SMTP_SSL("smtp.qq.com",465)
        server.login(my_sender,my_pass)
        server.sendmail(my_sender,[my_user],message.as_string())
        server.quit()
    except Exception:
        ret = False

    return ret

ret = mail()
if ret:
    print('邮件发送成功')
else:
    print('邮件发送失败')



