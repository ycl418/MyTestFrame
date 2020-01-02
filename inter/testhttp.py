# -*- coding: UTF-8 -*-
from inter.webkeys import HTTP

# 创建一个http请求库的实例对象
http = HTTP()
# 设置基础地址
http.setUrl('http://10.2.2.128:38080/interface/HTTP//')
# 授权
http.post('auth', None)
print(http.jsonres)
# 保存token
http.savejson('token', 'token')
print(http.relations)
# 添加头
http.addheader('token', '{token}')
# 注册
http.post('register', 'username=ycl02&pwd=2580&nickname=柚子&describe=柚子')
print(http.jsonres)
# 登录
http.post('login', 'username=ycl02&password=2580')
print(http.jsonres)
# 保存userid
http.savejson('userid', 'userid')
# 查看用户信息
http.post('getUserInfo', 'id={userid}')
print(http.jsonres)
# 注销
http.post('logout', None)
print(http.jsonres)
