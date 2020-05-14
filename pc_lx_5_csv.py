import requests,bs4,csv

#header 变个身去偷
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}


movies = []

#创建csv
csv_file = open('电影排行.csv','w',newline='',encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['序号','电影名称','评分','推荐语','链接'])

for i in range(1,11):
    #爬取链接
    url = 'https://movie.douban.com/top250?start={}&filter='.format((i-1)*25)

    res = requests.get(url,headers=header)

    bs = bs4.BeautifulSoup(res.text,'html.parser')

    ul = bs.find('ol',class_='grid_view')
    if ul is not None:
        for item in ul.find_all('li'):
            #防止找不到标签出错，try
            try:
                num = item.find('em').text
                title = item.find('div',class_='hd').find('a')
                rate = item.find('div',class_='star').find('span',class_='rating_num')
                tuijian = item.find('p',class_='quote').find('span')
                #if isinstance(tuijian,bs4.element.Tag):
                movies.append([num,title.text,rate.text,tuijian.text,title['href']])
            except:
                #错误是AttributeError: 'NoneType' object has no attribute 'find', 排雷是：<p class='quote'><span>.....</span></p>找不到
                #那么没有推荐语就为空，再增加到列表
                movies.append([num,title.text,rate.text,'',title['href']])
                continue
    else:
        print('爬取不到数据')
        break

#for i in movies:
#    writer.writerow(i)

#用writerows直接写入
writer.writerows(movies)
csv_file.close()

print(movies)