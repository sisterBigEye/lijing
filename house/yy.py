#-*- coding:utf-8 -*-
from functools import reduce
def fn(x, y):
 return x * 10 + y

def char2num(s):
   return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
print map(char2num,'13579')
print reduce(fn, map(char2num, '13579'))


def print_msg():
    msg = 'zen of python'

    # def printer():
    print(msg)
    return msg
    # return printer
#把print_msg函数指向another
another = print_msg()
print 'hihi'
#函数内的变量msg在调用该函数时可以可用，执行过后便不在可用了
print another
# another()


#闭包使得局部变量可以在函数外被调用
def print_msg1():
    msg = 'zen of python'

    def printer():
        print(msg)
    return printer
#把print_msg函数指向another
another1 = print_msg1()
print 'hhaa'
another1()

def foo():
    return 1

def bar():
    return foo
print (bar())
print(bar()())
print(foo())