import requests
from bs4 import BeautifulSoup
from queue import Queue
import re,os,threading,time,sys
#脚本超时
import socket
socket.setdefaulttimeout(1000)

from requests.adapters import HTTPAdapter

#网页编码
encoding = 'utf-8'

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget,QTextBrowser, QPushButton,QDesktopWidget,QLabel,QLineEdit,QTextEdit,QCheckBox,QGridLayout,QFileDialog,QVBoxLayout,QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal,QDateTime,QObject

#-----------------线程类--------------------
class DownThread(QObject):
    # 通过类成员对象定义信号
    down_pic = pyqtSignal(str)

    #重写 run 处理业务逻辑
    def run(self):
        



#=================窗口类====================
class DownPic(QWidget):
    current_file_dictory = "G:/"
    save_path = 'G:/'
    item_name = "BT1024 图片下载器 1.0"

    #
    def __init__(self):
        super().__init__()
        self.current_file_dictory = os.path.split(os.path.realpath(__file__))[0]
        self.save_path = self.current_file_dictory
        self.initUI()
        
    def initUI(self):

        #GUI布局内容
        caiUrl_lbn = QLabel("<font color='red'>采集地址：</font>")
        spage_btn = QLabel("起始页：")
        epage_btn = QLabel("结束页：")
        key_btn = QLabel('关键字：')
        savepath_btn = QLabel('保存路径：')
        info_btn = QLabel('采集信息：')

        self.setStyleSheet('height:30px')
        self.caiurl = QLineEdit()
        self.caiurl.setPlaceholderText('http://www.xxx/page')
        #self.caiurl.setStyleSheet('height:30px')
        self.spage = QLineEdit('1')
        self.epage = QLineEdit('2')
        self.key = QLineEdit('')
        self.savepath = QPushButton(self.current_file_dictory)
        self.info = QTextEdit()
        self.info.setStyleSheet('line-height:25px;padding:5px')

        self.caiji = QPushButton('开始')
        self.caiji.clicked.connect(self.caiji_Clicked)
        self.caiji.setStyleSheet('width:100px;height:40px;')
        self.caiji.setFixedSize(150,50)

        self.savepath.clicked.connect(self.savepath_Clicked)

        grid = QGridLayout()
        grid.addWidget(caiUrl_lbn,1,0,1,1)
        grid.addWidget(self.caiurl,1,1,1,1)
        grid.addWidget(spage_btn,2,0)
        grid.addWidget(self.spage,2,1)
        grid.addWidget(epage_btn,3,0)
        grid.addWidget(self.epage,3,1)
        grid.addWidget(key_btn,4,0)
        grid.addWidget(self.key,4,1)
        grid.addWidget(savepath_btn,5,0)
        grid.addWidget(self.savepath,5,1)
        grid.addWidget(info_btn,6,0)
        grid.addWidget(self.caiji,6,1)

        gridinfo = QGridLayout()
        gridinfo.addWidget(self.info,1,0)


        

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(gridinfo)

        self.setLayout(vbox)

        self.resize(750,550)
        self.center()
        self.setWindowTitle(self.item_name)
        self.setWindowIcon(QIcon('icon/icon.ico'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #保存路径
    def savepath_Clicked(self):
        filepath= QFileDialog.getExistingDirectory(self,directory=self.current_file_dictory)
        #print(filepath)
        self.savepath.setText(filepath)
        self.save_path = filepath


    def caiji_Clicked(self):
        if self.caiji.isEnabled():
            self.caiji.setEnabled(False)
        #------------- 开始采集 ------------------------
        start_page = int(self.spage.text())
        end_page = int(self.epage.text())
        caiji_lianjie = self.caiurl.text()
        if caiji_lianjie == '':
            self.showMsg('请填写采集地址')
            self.caiji.setEnabled(True)
            return
        self.info.setText(caiji_lianjie)

        if end_page>=start_page:
            urlQueue = Queue()
            for i in range(start_page,end_page+1):
                caiurl = caiji_lianjie + '&page='+str(i)
                urlQueue.put(caiurl)
            #保存任务日志
            self.Task_TXT(caiji_lianjie,start_page,end_page)

            startTime = time.time()
            threads = []
            referer = 'http://x.qcyghfzh.xyz/pw/'
            # 可以调节线程数， 进而控制抓取速度
            threadNum = 4
            for i in range(0, threadNum):
                t = threading.Thread(target=self.cj_List, args=(urlQueue,referer))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
                t.join()
            endTime = time.time()
            self.info.setText('完成共花费: %d 分钟' % (int(endTime - startTime)/60))
        #-----------------------------------------------------------
    
    #提示信息
    def showMsg(self,msg):
        messageBox = QMessageBox()
        messageBox.setWindowTitle('提示')
        messageBox.setText(msg)
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = messageBox.button(QMessageBox.No)
        buttonN.setText('取消')
        messageBox.exec_()

    #关闭事件
    def closeEvent(self, event):
        messageBox = QMessageBox()
        messageBox.setWindowTitle('提示')
        messageBox.setText('确定退出？')
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = messageBox.button(QMessageBox.No)
        buttonN.setText('取消')
        messageBox.exec_()
        if messageBox.clickedButton() == buttonY:
            event.accept()
        else:
            event.ignore()
    
    #------------------------------GUI结束-----------------------------------------------------


    #==============================爬虫开始===========================
    #headers
    def header(self,origin='',referer=''):
        '''定义header 请求来源，并标记了请求从什么设备，什么浏览器上发出'''
        headers = {
            'origin':origin,
            # 请求来源
            'referer':referer,
            # 请求来源
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
            # 标记了请求从什么设备，什么浏览器上发出
            }
        return headers

    #创建目录
    def mkdir(self,path):
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


    #下载图片,自动识别扩展名
    def downimg(self,imgQueue,saveName,orgin,referer): 
        '''下载图片'''
        while True:
            try:
                # 不阻塞的读取队列数据
                imgurl = imgQueue.get_nowait()
            except Exception as e:
                #print(e)
                self.info.setText(e)
                break
            info = '正在下载： ' + imgurl
            self.info.setText(info)

            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            try:
                start = time.time()
                #新文件名
                newName = saveName + imgurl[-15:]
                if os.path.exists(newName):
                    check_res = s.get(imgurl,timeout=5, headers=self.header(orgin,referer))
                    if os.path.getsize(newName) == check_res.iter_content(chunk_size=1024):
                        #print('图片已存在，下载下一张...')
                        self.info.setText('图片已存在，下载下一张...')
                        continue
                #img_res = requests.get(imgurl, stream=True,headers=header(orgin,referer))
                img_res = s.get(imgurl, timeout=10, stream=True, headers=self.header(orgin,referer))
                #print()
                self.info.setText('保存位置：{}'.format(newName))
                
                #如果请求并且响应成功
                if img_res.status_code==200:
                    #判断图片是否存储
                    if os.path.exists(newName):
                        if img_res.iter_content(chunk_size=1024)!=os.path.getsize(newName):
                            counter = 0 
                            f = open(newName, 'wb') 
                            for chunk in img_res.iter_content(chunk_size=1024): 
                                if chunk: 
                                    f.write(chunk) 
                                    f.flush() 
                                    counter += 1 
                            f.close()
                    else:
                        
                            counter = 0 
                            f = open(newName, 'wb') 
                            for chunk in img_res.iter_content(chunk_size=1024): 
                                if chunk: 
                                    f.write(chunk) 
                                    f.flush() 
                                    counter += 1 
                            f.close()
                    #判断图片是否下载完成,没有则继续下载
                    n=0
                    while os.path.getsize(newName) != img_res.iter_content(chunk_size=1024):
                        #print()
                        self.info.setText('第{}次下载...'.format(n))
                        n+=1
                        counter = 0 
                        f = open(newName, 'wb') 
                        for chunk in img_res.iter_content(chunk_size=1024): 
                            if chunk: 
                                f.write(chunk) 
                                f.flush() 
                                counter += 1 
                        f.close()
                        #下载5次则退出
                        if n>5:
                            break
                else:
                    #print()
                    self.info.setText('失败图片：{}'.format(imgurl))
                endt = time.time()
                imginfo = '已用时间：%.2f秒' % (endt-start)
                self.info.setText(imginfo)
            except requests.exceptions.RequestException as e:
                self.info.setText(e)




    #获取图片后缀名
    def img_type(self,header):
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

    #保存任务到TXT
    def Task_TXT(self,taskurl,spage,epage):
        '''保存采集任务到txt'''
        with open('{}/{}.txt'.format(self.save_path,time.strftime('%Y-%m-%d-%H%M%S')),'w',encoding='utf-8') as ftxt:
            ftxt.write('采集网址：{}\n\n'.format(taskurl))
            ftxt.write('起始页：{}\n\n'.format(spage))
            ftxt.write('结束页：{}\n\n'.format(epage))

    #采集内容
    def getText(self,url,referer):
        '''获取Text'''
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        #cj_res = s.get(url,headers=header(referer=referer))
        try:
            cj_res = s.get(url, timeout=5, headers=self.header(referer=referer))
            if cj_res.status_code==200:
                cj_res.encoding = encoding
                return cj_res.text
            else:
                return 'None'
        except requests.exceptions.RequestException as e:
                self.info.setText(e)
                self.info.setText('失败地址：{}'.format(url))
                return 'None'

    #列表采集
    def cj_List(self,urlQueue,referer):
        '''列表采集'''
        while True:
            try:
                # 不阻塞的读取队列数据
                url = urlQueue.get_nowait()
                # i = urlQueue.qsize()
            except Exception as e:
                self.info.setText(e)
                break
            self.info.setText('正在执行线程：%s, 采集地址： %s ' % (threading.currentThread().name, url))
            try:
                html = self.getText(url,referer)
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
                                if self.key.text()!='':
                                    if title.text.find(self.key.text())==-1:
                                        #找不到继续下一条
                                        continue
                                if cj_href.find('http://')==-1:
                                    cj_href=self.caiurl.text()[:self.caiurl.text().rfind('/')+1]+cj_href
                                
                                #===================详情页====================
                                #---------------------------------------------------------------
                                xqhtml = self.getText(cj_href,url)
                                if xqhtml!='None':
                                    #先创建文件夹
                                    self.mkdir('{}/{}'.format(self.save_path,title))
                                    xq = BeautifulSoup(xqhtml,'html.parser')
                                    xq_main = xq.find('div',class_='tpc_content')
                                    xq_pics = xq_main.find('div',id='read_tpc').find_all('img')
                                    p=0
                                    #创建多线程实例
                                    imgUrlQueue = Queue()
                                    for pic in xq_pics:
                                        #print(pic['src'])
                                        p+=1
                                        #下载图片
                                        #添加多线程任务
                                        imgUrlQueue.put(pic['src'])
                                    imgThreads = []
                                    imgThreadNum = 4
                                    imgorgin = 'http://x.qcyghfzh.xyz/pw/'
                                    saveName = '{}/{}/'.format(self.save_path,title)
                                    for l in range(0,imgThreadNum):
                                        imgt = threading.Thread(target=self.downimg,args=(imgUrlQueue,saveName,imgorgin,cj_href)) 
                                        imgThreads.append(imgt)
                                    for it in imgThreads:
                                        it.start()
                                    for it in imgThreads:
                                        # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
                                        it.join()
                                        

                                #---------------------------------------------------------------
            except Exception as e:
                self.info.setText(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dp = DownPic()
    sys.exit(app.exec_())