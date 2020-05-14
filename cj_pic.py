import requests,openpyxl
from bs4 import BeautifulSoup
import time

pics = []

#headers
def header(origin,referer):
    '''定义header 请求来源，并标记了请求从什么设备，什么浏览器上发出'''
    headers = {
        'origin':origin,
        # 请求来源
        'referer':referer,
        # 请求来源
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
        # 标记了请求从什么设备，什么浏览器上发出
        }
    return headers

def mkdir(path):
    '''创建目录'''
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        #print(path + ' 创建成功')


#cj_url = input('采集图片网址：')


#下载图片
def xiazaipic(url,saveName):
    '''下载图片'''
    import time
    info = '正在下载： ' + url
    #print(info,end="")
    #print("\b"*(len(info)*2),end="",flush=True)
    print(info)
    start = time.time()
    res = requests.get(url)
    pic = res.content
    with open(saveName,'wb') as fs:
        fs.write(pic)
        fs.flush()
        fs.close()
    end = time.time()
    print('所用时间：{}秒'.format(end-start))

def saveTXT(pics,saveName):
    '''保存图片链接到TXT文件'''
    #文件夹
    #保存路径目录
    dirname = 'G:/图片/美女/'+saveName+'/'
    mkdir(dirname)
    with open(dirname+saveName+'.txt','a+',encoding='utf-8') as fs:
        #fs.write(biaoti+' '+href+' \n')
        for item in pics:    
            fs.write(item+' \n')
    #写入再清空pics
    pics.clear()


def cjtu(url='',encoding='utf-8',referer=''):

    res = requests.get(url,headers=header('http://www.mmkx8.com',referer))

    res.encoding=encoding

    html = res.text

    cjcon = BeautifulSoup(html,'html.parser')

    tudiv = cjcon.find(class_='photo')

    #标题
    title = tudiv.find('h1').text
    title = title[:title.find('(')]
    #当前图数
    nownum = tudiv.find(class_='nowpage').text
    #总图数
    totalnum = tudiv.find(class_='totalpage').text

    #保存图片名字
    #picname = title+'_'+nownum+'.jpg'

    #保存路径目录
    #dirname = 'G:/图片/美女/'+title+'/'
    #mkdir(dirname)

    #图片地址
    picurl = tudiv.find('img')['src']
    
    #下载图片
    #xiazaipic(picurl,dirname+picname)
    pics.append(picurl)

    #下一张图片
    if int(nownum)<int(totalnum):
        nexturl = tudiv.find(class_='topmbx').find_all('a')[1]['href']
        nextpicurl = nexturl+tudiv.find(class_='big-pic').find('a') ['href']
        #print(nextpicurl)
        cjtu(url=nextpicurl,referer=url)


#cjtu(cj_url)

def start_list(url='',encoding='utf-8',referer=''):
    '''初始列表'''
    res = requests.get(url,headers=header('http://www.mmkx8.com',referer))
    res.encoding=encoding
    html = res.text
    cjlist = BeautifulSoup(html,'html.parser')

    #当前页数

    #总页数
    totalPageNum = cjlist.find(id='pageNum').find_all('a')
    totalPageNum = totalPageNum[len(totalPageNum)-1:][0] # 转为字符串
    totalPageNum = totalPageNum['href']
    
    totalPageNum = totalPageNum[totalPageNum.rfind('-')+1:totalPageNum.rfind('.')]
    #print(totalPageNum)

    for i in range(1,int(totalPageNum)+1):
        newurl = '{}list-{}.html'.format(url,i)
        pic_list(url=newurl)
        #time.sleep(1)



def pic_list(url='',encoding='utf-8',referer=''):
    '''列表'''
    res = requests.get(url,headers=header('http://www.mmkx8.com',referer))
    if res.status_code==200:
        res.encoding=encoding
        html = res.text
        cjlist = BeautifulSoup(html,'html.parser')

        #列表

        pic_lists = cjlist.find_all(class_='item masonry_brick')


        #详情
        for item in pic_lists:

            #链接
            lianjie = item.find('div',class_='img').find('a')
            href = lianjie['href']

            #标题
            biaoti = lianjie.find('img')['title']

            #print(href)
            info = '正在采集： ' + href
            #print(info,end="")
            #print("\b"*(len(info)*2),end="",flush=True)
            print(info)
            start = time.time()

            cjtu(url=href)
            saveTXT(pics,biaoti)

            end = time.time()
            print('所用时间：{}秒'.format(end-start))
            


            #with open('pic_list.txt','a+',encoding='utf-8') as fs:
            #    #fs.write(biaoti+' '+href+' \n')
            #    fs.write(href+' \n')
    else:
        print('爬取失败')


picurl = input('采集图片地址：')
picName = input('图集名称：')
#'http://www.mmkx8.com/renti/37626.html'
cjtu(url=picurl)
saveTXT(pics,picName)
