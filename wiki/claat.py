# class Parent(object):
#     '''
#     parent class
#     '''
#     numList = [1,2]
#     def numAdd(self, a, b):
#         return a+b
#
#     def a(self):
#         print(Parent.numAdd(self,1,2))
#
#
#
# c = Parent()
# print(c)
# print (Parent.numList)
#
# c.a()

def func():
    print("func() in one.py")

print("top-level in one.py")

if __name__ == "__main__":
    print("one.py is being run directly")
else:
    print("one.py is being imported into another module")