import datetime

#日期输出格式化 datetime => string
now = datetime.datetime.now()
print(now)

print (now.strftime('%Y-%m-%d %H:%M:%S'))


#日期输出格式化 string => datetime

t_str = '2015-4-07'

d = datetime.datetime.strptime(t_str, '%Y-%m-%d')
print (d)
print(type(d))