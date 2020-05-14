# 引入json模块
import json
# 创建一个列表a
a = [1,2,3,4]
# 使用dumps()函数，将列表a转换为json格式的字符串，赋值给b
b = json.dumps(a)
# 打印b
print(b)
# 打印b的数据类型
print(type(b))
# 使用loads()函数，将json格式的字符串b转为列表，赋值给c
c = json.loads(b)
# 打印c
print(c)
# 打印c的数据类型
print(type(c)) 