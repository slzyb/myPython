# 本地Chrome浏览器设置方法
from selenium import  webdriver #从selenium库中调用webdriver模块
import time

driver = webdriver.Chrome() # 设置引擎为Chrome，真实地打开一个Chrome浏览器
driver.get('https://localprod.pandateacher.com/python-manuscript/hello-spiderman/') 
time.sleep(2)

teacher = driver.find_element_by_id('teacher')
teacher.send_keys('必须是吴枫呀')
assistant = driver.find_element_by_name('assistant')
assistant.send_keys('都喜欢')
time.sleep(1)
button = driver.find_element_by_class_name('sub')
time.sleep(1)
button.click()
time.sleep(1)
driver.close()