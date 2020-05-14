import requests
url = 'https://static.pandateacher.com/Over%20The%20Rainbow.mp3'
res = requests.get(url)
con = res.content
o = open('lx3.mp3','wb+')
o.write(con)
o.close()