import time
import socket
socket.setdefaulttimeout(600)
url = 'https://p9.urlpic.xyz/pic20/upload/image/20200413/41309133985.jpg'
       #https://p9.urlpic.xyz/pic20/upload/image/20200413/41309133989.jpg
print(url[-15:])
for i in range(1,2):
    print(str(time.time()))

import os
url="ftp://ygdy8:ygdy8@y201.dygod.org:1132/[阳光电影www.ygdy8.com].冬眠.BD.720p.中文字幕.rmvb"
#os.system(r'"C:\Program Files (x86)\Thunder Network\Thunder\Program\ThunderStart.exe" {url}'.format(url=url))

import time
import requests
from requests.adapters import HTTPAdapter
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
print(time.strftime('%Y-%m-%d %H:%M:%S'))
try:
       r = s.get('https://p9.urlpic.xyz/pic20/upload/image/20200410/41009077768.jpg', timeout=5)
       print(r.text)
except requests.exceptions.RequestException as e:
       print(e)
       print(time.strftime('%Y-%m-%d %H:%M:%S'))
