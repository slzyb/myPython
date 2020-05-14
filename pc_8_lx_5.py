import requests
import json

api_url = 'http://openapi.tuling123.com/openapi/api/v2'
userid  = '608996'
apikey  = 'fa79596fd5ec4a2391e71e7852303f6d'

reqType = 0 #  输入类型:0-文本(默认)、1-图片、2-音频

codes = {
    '5000':'无解析结果',
    '6000':'暂不支持该功能',
    '4000':'请求参数格式错误',
    '4001':'加密方式错误',
    '4002':'无功能权限',
    '4003':'该apikey没有可用请求次数',
    '4005':'无功能权限',
    '4007':'apikey不合法',
    '4100':'userid获取失败',
    '4200':'上传格式错误',
    '4300':'批量操作超过限制',
    '4400':'没有上传合法userid',
    '4500':'userid申请个数超过限制',
    '4600':'输入内容为空',
    '4602':'输入文本内容超长(上限150)',
    '7002':'上传信息失败',
    '8008':'服务器错误',
    '0':'上传成功'
}


while True:

    data1 = {

        "reqType":reqType,
        "perception": {
            "inputText": {
                "text": input('我：')
            },
            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "信息路"
                }
            }
        },
        "userInfo": {
            "apiKey": apikey,
            "userId": userid
        }
    }
    #把字典转换为JSON 字符串格式，要不然 API 接口返回4000
    data = json.dumps(data1)
    #print(type(data))
    rs = requests.post(api_url,data=data)
    if rs.status_code==200:
        json_lt = rs.json()
        code = json_lt['intent']['code']
        if str(code) not in codes:
            print('小灵：'+json_lt['results'][0]['values']['text'])
            
        else:
            errmsg = json_lt['results'][0]['values']['text']
            print(errmsg)
            #print(codes[str(code)])
            break

    else:
        print('请求API接口错误')
        break