import requests,openpyxl
#from bs4 import BeautifulSoup

#headers
def  header(origin,referer):
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

url = 'https://www.zhihu.com/api/v4/members/zhang-jia-wei/articles'

loop = True

i = 1

author = '张佳玮'
wb=openpyxl.Workbook()
sheet=wb.active
sheet.title=author
sheet['A1'] = '标题'
sheet['B1'] = '摘要'
sheet['C1'] = '链接'
sheet['D1'] = '内容'

#不知道人家有多少数据
while loop:

    offset = i * 10
    i += 1

    params = {
        'include': 'data[*].comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info;data[*].author.badge[?(type=best_answerer)].topics',
        'offset': offset,
        'limit': '10',
        'sort_by': 'created'
    }
    print(offset)

    res = requests.get(url,params=params,headers=header('https://www.zhihu.com/people/zhang-jia-wei/posts','https://www.zhihu.com/people/zhang-jia-wei/posts?page='+str(i)))

    #请求成功
    if res.status_code==200:
        res.encoding = 'utf-8'
        jsons = res.json()
        art_list = jsons['data']
        is_end = jsons['paging']['is_end']
        for item in art_list:
            #print(item['title'])
            sheet.append([item['title'],item['excerpt'],item['url'],item['content']])
        if is_end:
            loop = False
    else:
        print('该网站设置防爬虫机制，爬取终止！')
        loop = False

wb.save('{}.xlsx'.format(author))
wb.close()