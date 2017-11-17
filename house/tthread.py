# -*- coding:utf-8 -*-
import threading

def a():
    print 'b'
    bb=[1,2,3]
    def c():
        while True:
            try:
                print bb.pop()
                print bb
            except IndexError:
                break
        print 'hi'


    threads = []

    while bb:
        # print 'ahha'
        thread = threading.Thread(target=c)
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)
    print len(threads)

    for thread in threads:
        print thread
        if not thread.is_alive():
            print("kill")
            threads.remove(thread)

a()