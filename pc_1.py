import requests

url = 'https://localprod.pandateacher.com/python-manuscript/crawler-html/sanguo.md'

res = requests.get(url)

#response对象的常用属性
#response.status_code   状态响应代码   检查请求是否成功
#response.content       把response对象转换为二进制数据
#response.text          把response对象转换为字符串数据
#response.encoding      定义response对象的编码

print(type(res))