# -*- coding: utf-8 -*-
a = {"孩子":1, "我们":5}
b = None
for d in a:
    if b!=None:
        b += ", "
    else:
        b = "{"
    b += "'" + str(d).decode("utf-8") + "' : " + str(a[d]).decode("utf-8")
    b += "}"
print b


#'python字典嵌套字典的情况下获取某个key的value

import types

#获取字典重点objkey对应的值，适用于字典嵌套
#dict:字典
#objkey:目标key
#default:找不到时返回的默认值

def dict_get(dict,objkey,default):
    tmp = dict
    for k,v in tmp.items():
        if k == objkey:
            return v
        else:
            if type(v) is types.DictType:
                ret = dict_get(v,objkey,default)
                if ret is not default:
                    return ret
    return default

dictest = {"result":{"code":"110002","msg":"设备序列号或验证码错误"}}
ret = dict_get(dictest,'msg',None)
ret =ret.decode('utf-8').encode('gb2312')
print(ret)