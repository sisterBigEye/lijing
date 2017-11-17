
# from collections import OrderedDict
#
# d={'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
# print d.items()
#
# print OrderedDict(sorted(d.items(), key=lambda t: t[0]))
#
# key=lambda t: t[1]
# print key
i=3

def func():
    global i
    a=[]
    i -= 1
    if i>0:
        a.append(i)

        func()
        print("wo")
    print a
    return a


print func()

