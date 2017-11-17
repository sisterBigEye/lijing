#-*- coding:utf-8 -*-
import json

# 序列化到文件中
with open('test.json', 'w') as fp:
    json.dump({'a':'str中国', 'c': True, 'e': 10, 'b': 11.1, 'd': None, 'f': [1, 2, 3], 'g':(4, 5, 6)}, fp, indent=4)

# 反序列化文件中的内容
with open('test.json', 'r') as fp:
   print json.load(fp)