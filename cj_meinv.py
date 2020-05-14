import requests,openpyxl
from bs4 import BeautifulSoup
from queue import Queue
import re,os,threading,time

pics = []

encoding = 'utf-8'

#采集信息收集

caiji_lianjie = input('采集网址：')
start_page = 1
end_page = 1
while True:
    try:
        start_page = int(input('采集起始页：'))
        end_page = int(input('采集结束页：'))
        break
    except ValueError:
        continue

#headers
def header(origin='',referer=''):
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

#创建目录
def mkdir(path):
    '''创建目录'''
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
def xiazaipic(url,saveName,orgin,referer):
    '''下载图片'''
    info = '正在下载： ' + url
    #print(info,end="")
    #print("\b"*(len(info)*2),end="",flush=True)
    print(info)
    start = time.time()
    res = requests.get(url,headers=header(orgin,referer))
    #如果请求并且响应成功
    if res.status_code==200:
        pic = res.content
        with open(saveName,'wb') as fs:
            fs.write(pic)
            fs.flush()
            fs.close()
    end = time.time()
    print('所用时间：{}秒'.format(end-start))



#下载图片,自动识别扩展名
def downimg(imgUrl,saveName,orgin,referer): 
    '''下载图片 自动识别扩展名,saveName中不要带 .xxx'''
    info = '正在下载： ' + imgUrl
    #print(info,end="")
    #print("\b"*(len(info)*2),end="",flush=True)
    print(info)
    start = time.time()
    img_res = requests.get(imgUrl, stream=True,headers=header(orgin,referer))
    saveName = saveName + img_type(img_res.headers)
    #如果请求并且响应成功
    if img_res.status_code==200:
        #判断图片是否存储
        if os.path.exists(saveName):
            if img_res.iter_content(chunk_size=1024)!=os.path.getsize(saveName):
                counter = 0 
                f = open(saveName, 'wb') 
                for chunk in img_res.iter_content(chunk_size=1024): 
                    if chunk: 
                        f.write(chunk) 
                        f.flush() 
                        counter += 1 
                f.close()
        else:
            
                counter = 0 
                f = open(saveName, 'wb') 
                for chunk in img_res.iter_content(chunk_size=1024): 
                    if chunk: 
                        f.write(chunk) 
                        f.flush() 
                        counter += 1 
                f.close()
    end = time.time()
    print('所用时间：{}.2f秒'.format(end-start))



#获取图片后缀名
def img_type(header):
    '''获取图片后缀名'''
    # 获取文件属性
    image_attr = header['Content-Type']
    pattern = 'image/([a-zA-Z]+)'
    suffix = re.findall(pattern,image_attr,re.IGNORECASE)
    if not suffix:
        suffix = 'png'
    else :
        suffix = suffix[0]
    # 获取后缀
    if re.search('jpeg',suffix,re.IGNORECASE):
        suffix = 'jpg'
    return '.' + suffix


#采集内容
def getText(url,referer):
    '''获取Text'''
    cj_res = requests.get(url,headers=header(referer=referer))
    if cj_res.status_code==200:
        cj_res.encoding = encoding
        return cj_res.text
    else:
        return 'None'

#列表采集
def cj_List(urlQueue,referer):
    '''列表采集'''
    while True:
        try:
            # 不阻塞的读取队列数据
            url = urlQueue.get_nowait()
            # i = urlQueue.qsize()
        except Exception as e:
            break
        print('正在执行线程：%s, 采集地址： %s ' % (threading.currentThread().name, url))
        try:
            html = getText(url,referer)
            if html!='None':
                cjcon = BeautifulSoup(html,'html.parser')
                maindiv = cjcon.find('div',id='main')
                zutis = maindiv.find_all('tr')
                for zuti in zutis:
                    if zuti.find('h3'):
                        cj_zuti = zuti.find('h3')
                        cj_href = cj_zuti.find('a')['href']
                        #去掉置顶
                        if cj_href.find('read.php')==-1:
                            #print(zuti.find('h3'))
                            #标题
                            title = cj_zuti.text
                            if cj_href.find('http://')==-1:
                                cj_href=caiji_lianjie[:caiji_lianjie.rfind('/')+1]+cj_href
                            
                            #===================详情页====================
                            #---------------------------------------------------------------
                            xqhtml = getText(cj_href,url)
                            if xqhtml!='None':
                                #先创建文件夹
                                mkdir('G:/采集图片/{}'.format(title))
                                xq = BeautifulSoup(xqhtml,'html.parser')
                                xq_main = xq.find('div',class_='tpc_content')
                                xq_pics = xq_main.find('div',id='read_tpc').find_all('img')
                                p=0
                                for pic in xq_pics:
                                    #print(pic['src'])
                                    p+=1
                                    #下载图片
                                    #xiazaipic(pic['src'],'G:/采集图片/{}/{}_{}.jpg'.format(title,title,p),'http://x.qcyghfzh.xyz/pw/',cj_href)
                                    downimg(pic['src'],'G:/采集图片/{}/{}_{}'.format(title,title,p),'http://x.qcyghfzh.xyz/pw/',cj_href)

                            #---------------------------------------------------------------
        except Exception as e:
            print(e)


def main():
    if end_page>start_page:

        urlQueue = Queue()#[urlQueue.put('http://www.qiumeimei.com/image/page/{}'.format(i)) for i in range(1,14)]
        for i in range(start_page,end_page+1):
            caiurl = caiji_lianjie + '&page='+str(i)
            urlQueue.put(caiurl)
            info = '正在采集： ' + caiurl
            print(info,end="")
            print("\b"*(len(info)*2),end="",flush=True)

        startTime = time.time()
        threads = []
        referer = 'http://x.qcyghfzh.xyz/pw/'
        # 可以调节线程数， 进而控制抓取速度
        threadNum = 4
        for i in range(0, threadNum):
            t = threading.Thread(target=cj_List, args=(urlQueue,referer))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
            t.join()
        endTime = time.time()
        print('完成共花费: %.2f 秒' % (endTime - startTime))

main()        

#cj_List('http://x.qcyghfzh.xyz/pw/thread.php?fid=21&page=1','http://x.qcyghfzh.xyz/pw/thread.php?fid=21')

        




