#-*- coding:utf-8 -*-
from multiprocessing import Process,Pool,Queue

import os,time,random
#子进程要执行的代码

# def run_proc(name):
#     print('Run child process  %s (%s)...'%(name,os.getpid()))
#
#
# if __name__=='__main__':
#     print('Parent process %s.' %os.getpid())
#     p=Process(target=run_proc,args=('test',))
#     print('Child process will start ')
#     p.start()
#     p.join()
#     print('Child process end.')
# def long_time_task(name):
#     print'Run task %s (%s)...'%(name,os.getpid())
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print'Task %s runs %0.2f seconds'%(name,(end-start))
#
# if __name__=='__main__':
#     print('Parent process %s.'%os.getpid())
#     p=Pool()
#     for i in range(5):
#         p.apply_async(long_time_task,args=(i,))
#     print('Waiting for all subprocess done...')
#     p.close()
#     p.join()
#     print('All subprocesses done')

# from multiprocessing import Pool
# import os, time, random
#
# def long_time_task(name):
#     print 'Run task %s (%s)...' % (name, os.getpid())
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print 'Task %s runs %0.2f seconds.' % (name, (end - start))
#
# if __name__=='__main__':
#     print 'Parent process %s.' % os.getpid()
#     p = Pool(5)
#     for i in range(5):
#         p.apply_async(long_time_task, args=(i,))
#     print 'Waiting for all subprocesses done...'
#     p.close()
#     p.join()
#     print 'All subprocesses done.'

def write(q):
    for value in ['A','B','C']:
        print('put %s to queue..'%value)
        q.put(value)
        #等待一会，可以使得两个进程交替进行
        time.sleep(random.random())

def read(q):
    while True:
        value = q.get(True)
        print('Get %s from queue.'%value)

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write,args=(q,))
    pr = Process(target=read,args=(q,))

    pw.start()
    pr.start()
    #等待pw结束
    pw.join()
    # # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
