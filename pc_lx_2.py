import requests
url = 'https://res.pandateacher.com/2019-01-12-15-29-33.png'
res = requests.get(url)
con = res.content
o = open('lx2.png','wb+')
o.write(con)
o.close()