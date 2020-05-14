import requests,json

#请求头
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '246',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #'Cookie': 'OUTFOX_SEARCH_USER_ID=-296483360@10.169.0.84; JSESSIONID=aaapt3vinF4iUf-etrlgx; OUTFOX_SEARCH_USER_ID_NCOO=1199577077.7390819; ___rl__test__cookies=1587179727848',
    'Host': 'fanyi.youdao.com',
    'Origin': 'http://fanyi.youdao.com',
    'Referer': 'http://fanyi.youdao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
    'X-Requested-With': 'XMLHttpRequest'
}

url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

session = requests.session()

while True:
    fanyi = input('\n输入你要翻译的文字：\n')    

    #语种代码
    yuzhongdaima = ['AUTO','zh-CHS','en','ja','ko','fr','de','ru','es','pt','it','vi','id','ar']
    #语种
    yuzhong      = ['自动检测','中文','英语','日语','韩语','法语','德语','俄语','西班牙语','葡萄牙语','意大利语','越南语','印尼语','阿拉伯语']
    #提交数据
    data1 = {
        'i': fanyi,
        'from': yuzhongdaima[0],
        'to': yuzhongdaima[0],
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        #'salt': '15871797278504',
        #'sign': 'c9802f02ebc3c6b4c3eba6b1cec4d611',
        #'ts': '1587179727850',
        #'bv': 'ec579abcd509567b8d56407a80835950',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION'
    }
    #print(data1)


    result = session.post(url,headers=headers,data=data1)
    if result.status_code==200:
        jsons = result.json()
        fy = jsons['translateResult'][0][0]['tgt']
        print(fy)
        continues = input('\n回车继续翻译，输入Q退出！\n')
        if continues == 'q' or continues=='Q':
            break
    else:
        print('连接服务器失败！')
        break
        

