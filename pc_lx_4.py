import requests,bs4

#header 变个身去偷
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}


movies = []

for i in range(1,11):
    #爬取链接
    url = 'https://movie.douban.com/top250?start={}&filter='.format((i-1)*25)

    res = requests.get(url,headers=header)

    bs = bs4.BeautifulSoup(res.text,'html.parser')

    ul = bs.find('ol',class_='grid_view')

    for item in ul.find_all('li'):
        #防止找不到标签出错，try
        try:
            num = item.find('em').text
            title = item.find('div',class_='hd').find('a')
            rate = item.find('div',class_='star').find('span',class_='rating_num')
            tuijian = item.find('p',class_='quote').find('span')
            #if isinstance(tuijian,bs4.element.Tag):
            movies.append([num,title.text,title['href'],rate.text,tuijian.text])
        except:
            #错误是AttributeError: 'NoneType' object has no attribute 'find', 排雷是：<p class='quote'><span>.....</span></p>找不到
            #那么没有推荐语就为空，再增加到列表
            movies.append([num,title.text,title['href'],rate.text,''])
            continue
        

print(movies)

