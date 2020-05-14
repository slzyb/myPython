# 引用requests库
import requests
# 引用BeautifulSoup库
from bs4 import BeautifulSoup

# 获取数据
res_foods = requests.get('http://www.xiachufang.com/explore/')
# 解析数据
bs_foods = BeautifulSoup(res_foods.text,'html.parser')

# 查找包含菜名和URL的<p>标签
tag_name = bs_foods.find_all('p',class_='name')
# 查找包含食材的<p>标签
tag_ingredients = bs_foods.find_all('p',class_='ing ellipsis')
# 创建一个空列表，用于存储信息
list_all = []
# 启动一个循环，次数等于菜名的数量
for x in range(len(tag_name)):
    # 提取信息，封装为列表。注意此处使用的是<p>标签，而之前是<a>
    list_food = [tag_name[x].text.strip(),tag_name[x].find('a')['href'],tag_ingredients[x].text.strip()]
    # 将信息添加进list_all    
    list_all.append(list_food)
# 打印
print(list_all)

# 以下是另外一种解法

# 查找最小父级标签
list_foods = bs_foods.find_all('div',class_='info pure-u')
# 创建一个空列表，用于存储信息
list_all = []

for food in list_foods:
    # 提取第0个父级标签中的<a>标签
    tag_a = food.find('a')
    # 菜名，使用strip()函数去掉了多余的空格
    name = tag_a.text.strip()
    # 获取URL
    URL = 'http://www.xiachufang.com'+tag_a['href']
    # 提取第0个父级标签中的<p>标签
    tag_p = food.find('p',class_='ing ellipsis')
    # 食材，使用strip()函数去掉了多余的空格
    ingredients = tag_p.text.strip()
    # 将菜名、URL、食材，封装为列表，添加进list_all
    list_all.append([name,URL,ingredients])

# 打印
print(list_all)