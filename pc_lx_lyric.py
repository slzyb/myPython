# 直接运行代码就好
import requests,json,re
# 引用requests模块

def  header(origin,referer):
    '''
    定义header 请求来源，并标记了请求从什么设备，什么浏览器上发出
    '''
    headers = {
        'origin':origin,
        # 请求来源
        'referer':referer,
        # 请求来源
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
        # 标记了请求从什么设备，什么浏览器上发出
        }
    return headers

def illegal_char(s):
    s = re \
        .compile( \
        u"[^"
        u"\u4e00-\u9fa5"
        u"\u0041-\u005A"
        u"\u0061-\u007A"
        u"]+") \
        .sub('', s)
    return s

def lyric(gcurl,music_url):
    '''
    获取歌词\n
    gcurl：歌词url xhr\n
    music_url：音乐url\n

    '''
    res_lyric = requests.get(gcurl,headers=header('https://y.qq.com',music_url))
    # 通过 res_lyric.text 可知含有 MusicJsonCallback(...) res_lyric不能直接用res_lyric.json(),先去掉  MusicJsonCallback(...)再用json.loads 转换成标准JSON格式

    json_lyric = json.loads(res_lyric.text[res_lyric.text.find('(')+1:res_lyric.text.find(')')])
    #json_lyric = res_lyric.json()
    #处理一下歌词
    gc = json_lyric['lyric'].replace('&#10;','换行')
    #print(illegal_char(gc).replace('换行','\n'))
    #exit()
    return illegal_char(gc).replace('换行','\n')

#url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid=102340965'
url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
for x in range(5):
    params = {
    'ct':'24',
    'qqmusic_ver': '1298',
    'new_json':'1',
    'remoteplace':'sizer.yqq.song_next',
    'searchid':'64405487069162918',
    't':'0',
    'aggr':'1',
    'cr':'1',
    'catZhida':'1',
    'lossless':'0',
    'flag_qc':'0',
    'p':str(x+1),
    'n':'20',
    'w':'周杰伦',
    'g_tk':'5381',
    'loginUin':'0',
    'hostUin':'0',
    'format':'json',
    'inCharset':'utf8',
    'outCharset':'utf-8',
    'notice':'0',
    'platform':'yqq.json',
    'needNewCode':'0'    
    }
    # 将参数封装为字典
    res_music = requests.get(url,params=params)
    # 调用get方法，下载这个字典
    json_music = res_music.json()
    # 使用json()方法，将response对象，转为列表/字典
    list_music = json_music['data']['song']['list']
    # 一层一层地取字典，获取歌单列表
    for music in list_music:
    # list_music是一个列表，music是它里面的元素
        print(music['name'])
        # 以name为键，查找歌曲名
        print('所属专辑：'+music['album']['name'])
        # 查找专辑名
        print('播放时长：'+str(music['interval'])+'秒')
        # 查找播放时长
        music_url = 'https://y.qq.com/n/yqq/song/'+music['mid']+'.html'
        print('播放链接：'+music_url)
        # 查找播放链接
        print('-'*20)
        print(lyric('https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid={}'.format(music['id']),music_url))
        print('-'*20+'\n\n')