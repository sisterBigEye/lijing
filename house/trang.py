#-*- coding:utf-8 -*-
def triangles():
    L = [1]
    while True:
        yield L
        L.append(0)
        L=[L[i-1]+L[i] for i in range(len(L))]
n = 1
for t in triangles():
    print(t)
    n=n+1
    if n == 10:
        break

# L=[]
# for i  in range(5):
#     # L=[1]+[2]+[3]
#     L=[i]+[i+1]
# print L
# L=[1,2,1,0]
# print L[0]
# print L[-1]

# L=[L[i-1]+L[i] for i in range(len(L))]
# print L