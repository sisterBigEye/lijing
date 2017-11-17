#-*-coding:utf-8 -*-
# from loogg import *
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger=logging.getLogger('logger_logger.child')

def outer(func):
    def inner():
        print("记录日志开始")
        func() #业务函数
        print('记录日志结束')
        logger.debug("this is a decottteee msg!")
        return 1
    return inner

@outer
def foo():
    print("foo")

# foo = outer(foo)
foo()



#不带参数的装饰器
# def tag(func):
#     def wrapper(text):
#         value = func(text)
#         return "<p>" + value +"</p>"
#
#     return wrapper
#
# @tag
# #业务函数
# def my_upper(text):
#     value = text.upper()
#     return value
#
#
# print(my_upper('hello'))

#带参数的装饰器

def tag(name):
    def deco(func):
        def wrapper(text):
            value=func(text)
            return "<{name}>{value}</{name}>".format(name=name,value=value)
        return wrapper
    return deco

@tag('p')
#业务函数
def my_upper(text):
    value = text.upper()
    return value

print(my_upper('hello'))

#装饰器在类中
# class A(object):
#     def outer(func):
#         def inner(self):
#             print("ttt")
#             r=func(self)
#             print("33")
#             return r
#         return inner
#     @outer
#     def f(self):
#         print('000')
#
# obj = A()
# obj.f()


#装饰器不在类中
# def outer(func):
#     def inner(self):
#         print("222")
#         r=func(self)
#         print("3333")
#         return r
#     return inner
# class  S(object):
#     @outer
#     def f(self):
#         print("000")
# a = S()
# a.f()

