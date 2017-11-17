#-*- coding:utf-8 -*-

class P(object):
    numlist = []
    def numadd(self,a,b):
        return a+b

class C(P):
    print "aaaa"
    def dd(self,c):
        return c

c=C()
C.numlist.extend(range(10))
print C.numlist
print"2+5 = ",c.numadd(2,5)
print c.dd(5)