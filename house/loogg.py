# -*- coding:utf-8 -*-
from datetime import datetime as dt
import logging
import functools

log_file="./basic_logger.log"
log_level = logging.DEBUG

logger = logging.getLogger('loggingmodule.NomalLogger')
handler = logging.FileHandler(log_file)
formatter=logging.Formatter('[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_level)


logger.debug("this is a debug msg!")
logger.info("this is a info msg!")
logger.warn("this is a warn msg!")
logger.error("this is a error msg!")
logger.critical("this is a critical msg!")

# def log(func):
#     print('['+str(dt.now())+']'+func.__name__)
# log(func)

#因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。

# #不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的
# def log(func):
#     @functools.wraps(func)
#     def wrapper(*args,**kwargs):
#         print('['+str(dt.now())+']'+func.__name__)
#         return func(*args,**kwargs)
#     return wrapper
# # 让装饰器可以装饰任何函数，而不用管那个函数又多少个参数。使用Python的可变参数 *args 和关键字参数 **kwargs 即可
# # func =log(func)
# @log
# def func(msg):
#     print('--&gt;' +msg)
# func('hahh')
#
# #带参数的装饰器
# def log1(is_show=True):
#     def decorator(func):
#         def wrapper(*args,**kwargs):
#             if is_show:
#                 print('['+str(dt.now())+']'+func.__name__)
#             return func(*args,**kwargs)
#         return wrapper
#     return  decorator
#
# @log1(False)#False不显示
# def func1(msg):
#     print('--&gt;' +msg)
# func1('hahh')
#

# def log(a):
#     def decorator(func):
#         def wrapper(*args,**kwargs):
#             print a + func.__name__
#             return func(*args,**kwargs)
#         return wrapper
#     return decorator
#
# @log('hello')
# def see(tmp):
#     print "i see you "+tmp
#     return tmp
#
# see('soso')
#
#

