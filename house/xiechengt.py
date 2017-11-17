#-*- coding:utf-8 -*-
from itertools import islice
import logging

log_file = 'xiecheng.log'
level = logging.DEBUG

logger = logging.getLogger('shengchengqi')
handler = logging.FileHandler(log_file)
formatter = logging.Formatter('[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s')

handler.setFormatter(formatter)
logger.setLevel(level)
logger.addHandler(handler)


def c():
    r='adafg'
    while True:
        n=yield r
        logger.info('这里出错了吗？')
        print n

g = c()
print g.next()
print g.send('a')
print g.send('g')
print list(islice(g,0,6,2))


#迭代器
class Fib:
    def __init__(self):
        self.prev = 0
        self.curr = 1
    def __iter__(self):
        return self
    def next(self):
        value = self.curr
        self.curr += self.prev
        self.prev = value
        return value
f = Fib()
print list(islice(f, 0, 10))

#生成器
def fib():
    prev, curr = 0, 1
    while True:
        yield curr
        prev, curr = curr, curr + prev
f = fib()
print list(islice(f, 0, 10))



def gen():
    value=0
    while True:
        receive=yield value
        print "haha"+str(receive)
        if receive=='e':
            break
        # value = 'got: %s' % receive

g=gen()
print(g.send(None))
print(g.send('aaa'))
print(g.send(3))
# print(g.send('e'))
# print g.next()
# print g.next()
# print g.next()
# print g.next()
# print g.next()
# print list(islice(g, 0, 5))
