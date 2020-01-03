# coding = utf-8

from inter.webkeys import HTTP
import inspect

"""
测试反射
"""
http = HTTP()

# getattr()表示从http这个实例里面获取addheader的属性或者方法
# func就等价于http.addheader
func = getattr(http, 'addheader')
# 反射获取关键字参数列表
s = inspect.getfullargspec(func).__str__()
s = s[s.find('args=')+5:s.find(', varargs')]
# 将字符串转为列表
s = eval(s)
s.remove('self')
print(s)