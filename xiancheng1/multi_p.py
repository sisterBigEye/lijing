#-*- coding:utf-8 -*-
from time import ctime,sleep
import threading


#重写thread。threading
class MyThread( threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args


    def run(self):
        apply(self.func,self.args)




def music(func):
    for i in range(2):
        print" i was listenning to %s. %s" %(func,ctime())
        sleep(1)

def move(func):
    for i in range(2):
        print "i was at the  %s ! %s" %(func,ctime())
        sleep(5)


athreads = []
t1 = threading.Thread(target=music,args=(u'小鸭子',))
athreads.append(t1)
t2 = threading.Thread(target=move,args=(u'蜘蛛侠',))
athreads.append(t2)

# if __name__=='__main__':
#     music(u'小鸭子')
#     move(u'阿凡达')
#     print "all over %s" %ctime()
if __name__ == '__main__':
    for t in athreads:
        t.setDaemon(True)
        t.start()

    t.join()

    print "all over %s" %ctime()


