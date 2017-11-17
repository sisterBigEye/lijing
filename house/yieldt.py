#-*- coding:utf-8 -*-
import Queue

def tt():
    for x in xrange(4):
        print 'tt'+str(x)
        yield

def gg():
    for x in xrange(4):
        print 'xx'+str(x)
        yield


class Task():
    def __init__(self):
        self._queue = Queue.Queue()

    def add(self,gen):
        self._queue.put(gen)

    def run(self):
        while not self._queue.empty():
            for i in xrange(self._queue.qsize()):
                try:
                    gen = self._queue.get()
                    gen.send(None)
                except StopIteration:
                    pass
                else:
                    self._queue.put(gen)


t=Task()
t.add(tt())
t.add(gg())
t.run()


#例2
def thread1():
    for x in range(4):
        yield x

def thread2():
    for x in range(4,8):
        yield x

threads=[]
threads.append(thread1())
threads.append(thread2())

def run(threads):
    for t in threads:
        try:
            print t.next()
        except StopIteration:
            pass
        else:
            threads.append(t)
run(threads)
