import time

# 本地Chrome浏览器设置方法
from selenium import webdriver #从selenium库中调用webdriver模块
driver = webdriver.Chrome() # 设置引擎为Chrome，真实地打开一个Chrome浏览器

driver.get('https://localprod.pandateacher.com/python-manuscript/hello-spiderman/') # 打开网页
time.sleep(60)#停留一分钟
driver.close() # 关闭浏览器

#---------------------------------