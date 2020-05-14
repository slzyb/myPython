import requests

#请求头
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}

#创建会话
xs_s = requests.session()

#登录地址
url = 'https://www.xslou.com/login.php'#https://www.xslou.com/login.php?do=submit

#登录POST数据
data1 = {
    'username': input('请输入用户名：'),
    'password': input('请输入密码：'),
    'usecookie': 0,
    'action': 'login',
    'submit': '登录'
}

print(xs_s.post(url,headers=headers,data=data1))
