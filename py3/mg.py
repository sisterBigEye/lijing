import types
def gen():
    for x in range(4):
        tmp = yield x
        if tmp =='hello':
            print ('world')
        else:
            print (str(tmp))
g = gen()
print (g)
print (isinstance(g,types.GeneratorType))

print (g.__next__())


# 上一次调用next,执行到yield 0暂停，再次执行恢复环境，给tmp赋值(注意：这里的tmp的值并不是x的值，而是通过send方法接受的值)，由于我们没有调用send方法，所以
# tmp的值为None,此时输出None，并执行到下一次yield x,所以又输出1
print (g.__next__())


#   上一次执行到yield 1后暂停，此时我们send('hello')，那么程序将收到‘hello'，并给tmp赋值为’hello',此时tmp=='hello'为真，所以输出'world',并执行到下一次yield 2,所以又打印出2.（next()等价于send(None)）
#       当循环结束，将抛出StopIteration停止生成器。
print (g.send('hello'))
