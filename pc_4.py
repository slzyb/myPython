import requests
from bs4 import  BeautifulSoup

# 请求html，得到response
res_music = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=55089861925200692&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w=%E5%85%94%E5%AD%90%E7%89%99&g_tk_new_20200303=2142659970&g_tk=2142659970&loginUin=28986765&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0')

# 使用json()方法，将response对象，转为列表/字典
json_music = res_music.json()
# 一层一层地取字典，获取歌单列表
list_music = json_music['data']['song']['list']
# list_music是一个列表，music是它里面的元素
for music in list_music:
    # 以name为键，查找歌曲名
    print(music['name'])
    # 查找专辑名
    print('所属专辑：'+music['album']['name'])
    # 查找播放时长
    print('播放时长：'+str(music['interval'])+'秒')
    # 查找播放链接
    print('播放链接：https://y.qq.com/n/yqq/song/'+music['mid']+'.html')
    # 查找url
    print('文件地址：{}\n\n'.format(music['url']))
    