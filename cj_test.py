import requests

from bs4 import BeautifulSoup

url = 'http://x.qcyghfzh.xyz/pw/thread.php?fid=5'

#print(url[:url.rfind('/')+1])

#采集信息收集

keyword = input('查找关键字：')
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

lists = {}

def  caiji(url,encoding='utf-8'):

    res = requests.get(url)

    res.encoding=encoding

    html = res.text

    cjcon = BeautifulSoup(html,'html.parser')

    items = cjcon.find_all('h3')


    for item in items:
        #标题
        title = item.find('a')
        #链接
        href = title['href']
        if href.find('http://')==-1:
            href=caiji_lianjie[:caiji_lianjie.rfind('/')+1]+href
        if title.text.find(keyword)!=-1:
            lists[title.text]=href
            #print(title.text)

def main():
    if end_page>start_page:
        for i in range(start_page,end_page+1):
            caiurl = caiji_lianjie + '&page='+str(i)
            info = '正在采集： ' + caiurl
            print(info,end="")
            print("\b"*(len(info)*2),end="",flush=True)
            caiji(caiurl)
    print('\n\n采集内容完成。\n')
    txtname = keyword + '.html'
    with open(txtname,'a+',encoding='utf-8') as cj:
        cj.write('''
        <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>{}</title>
        </head><body>'''.format(keyword))
        for k,v in lists.items():
            cj.write('<a href="{}" target="_blank">{}</a><br /><br />'.format(v,k))
        cj.write('''
        </body>
        </html>
        ''')

main()

#print(lists)