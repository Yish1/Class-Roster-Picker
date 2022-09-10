# -*- coding: utf-8 -*-


import sys,os
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from win32api import MessageBox
from win32con import MB_OK, MB_ICONWARNING

big = False
running = False

name = True
a = '''胡杰峰
黄嘉庆
龙飞
文理奥
柳一龙
罗欣悦
胡炳宏
孙博略
曾虹蜜
周子越
罗佳将
邹俊洋
薛明健
谢诚志
苏紫航
陈天意
邱泽
欧帆
罗正锟
戎智涵
刘泽楠
丁杰林
卢萱煊
胡宏伟
张世杰
尹傲为
王尊
祝祯鸿
劳汉文
杨奕璇
谭湘莹
胡淇
张家鑫
沈艳玲
陈丙峰
肖景元
黄炜杰
陈涛
钟涓
刘海鹏
谢作怡
陈泽钜
王俊'''

seed = False
choud = False

def name():
    with open('名单.txt', 'w') as f:
        print(f.truncate())
        print(f.write(a))


try:
    wordlist3 = ['胡杰峰','黄嘉庆','龙飞','文理奥','柳一龙','罗欣悦','胡炳宏','孙博略','曾虹蜜','周子越','罗佳将','邹俊洋','薛明健','谢诚志','苏紫航','陈天意','邱泽',
'欧帆','罗正锟','戎智涵','刘泽楠','丁杰林','卢萱煊','胡宏伟','张世杰','尹傲为','王尊','祝祯鸿','劳汉文','杨奕璇','谭湘莹','胡淇','张家鑫','沈艳玲','陈丙峰','肖景元',
'黄炜杰','陈涛','钟涓','刘海鹏','谢作怡','陈泽钜','王俊']
    name_list = wordlist3
except:

    name()
    name = False

    name_list = ['胡杰峰','黄嘉庆','龙飞','文理奥','柳一龙','罗欣悦','胡炳宏','孙博略','曾虹蜜','周子越','罗佳将','邹俊洋','薛明健','谢诚志','苏紫航','陈天意','邱泽',
'欧帆','罗正锟','戎智涵','刘泽楠','丁杰林','卢萱煊','胡宏伟','张世杰','尹傲为','王尊','祝祯鸿','劳汉文','杨奕璇','谭湘莹','胡淇','张家鑫','沈艳玲','陈丙峰','肖景元',
'黄炜杰','陈涛','钟涓','刘海鹏','谢作怡','陈泽钜','王俊']


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.RowLength = 0
        try:
            from os import path as pathq
            icon_path = pathq.join(pathq.dirname(__file__), './logo.ico')

            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path))  # 这是对的。
            MainWindow.setWindowIcon(icon)
        except:
            pass
        # self.setupUi(MainWindow())

    def setupUi(self, MainWindow):
        #以下课直接粘贴生成的setupui代码
        MainWindow.setObjectName("13班点名器By Yish")
        MainWindow.resize(460, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30,45, 470, 150))#主体
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(50)#主体大小
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(75, 220, 111, 61))#开始按钮
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(283, 220, 111, 61))#结束按钮
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(10, 10, 50, 30))#关于
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(12, 420, 435, 250))#统计
        self.listWidget.setObjectName("listWidget")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.listWidget.setFont(font)
        self.listWidget.setFocusPolicy(QtCore.Qt.WheelFocus)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 375, 210, 21))#文字
        self.label_2.setObjectName("label_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 320, 111, 35))#查看点过的名字
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(360, 320, 75, 35))#连抽模式
        self.pushButton_6.setObjectName("pushButton_6")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(580, 260, 89, 20))#连抽输入框
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText('2')
        self.lineEdit.setStyleSheet('''
        QListView, QLineEdit { 
            color: #D2D2D2; 
            background-color:#29292C;
            selection-color: #29292C; 
            border: 2px groove #29292C; 
            border-radius: 10px; 
            padding: 2px 4px; 
        } 
        QLineEdit:focus { 
            color: #D2D2D2; 
            selection-color: #29292C; 
            border: 2px groove #29292C; 
            border-radius: 10px; 
            padding: 2px 4px; 
        } 
        
                ''')
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(525, 260, 56, 21))#连抽人数
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet('color:white;background:#222225')
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(679, 250, 111,40))#连抽开始
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(503, 20, 353, 221))#连抽列表
        font = QtGui.QFont()
        font.setPointSize(20)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.listWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listWidget_2.setObjectName("listWidget_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 874, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.pushButton.clicked.connect(self.start)

        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_5.clicked.connect(self.showHistory)


        self.pushButton_7.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.pushButton_6.clicked.connect(self.showContinue)
        self.pushButton_7.clicked.connect(self.ten)
        self.pushButton_6.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.pushButton.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.pushButton_2.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.pushButton_9.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        #以上可以修改
        self.pushButton_5.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        #以上可以修改
        self.centralwidget.setStyleSheet('''
             QWidget#centralwidget{
             color:#222225;
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-right:1px solid #222225;
             border-left:1px solid #444444;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-left-radius:10px;
             border-bottom-right-radius:10px;
             }

             ''')
        self.close_widget = QtWidgets.QWidget(self.centralwidget)
        self.close_widget.setGeometry(QtCore.QRect(365, 0, 90, 30))
        self.close_widget.setObjectName("close_widget")
        self.close_layout = QGridLayout()  # 创建左侧部件的网格布局层
        self.close_widget.setLayout(self.close_layout)  # 设置左侧部件布局为网格

        self.left_close = QPushButton("✖️")  # 关闭按钮
        self.left_close.clicked.connect(MainWindow.close)
        self.left_visit = QPushButton("")  # 空白按钮
        self.left_visit.clicked.connect(MainWindow.big)
        self.left_mini = QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(MainWindow.mini)
        self.close_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.close_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.close_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_close.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(20, 20)  # 设置按钮大小
        self.left_mini.setFixedSize(20, 20)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.pushButton_9.clicked.connect(self.cmxz)
        self.label_2.setStyleSheet('color:white')

        self.scc = '''
         QListWidget{background-color:#2B2B2B;color:white}
         /*垂直滚动条*/
         QScrollBar:vertical{
             width:12px;
             border:1px solid #2B2B2B;
             margin:0px,0px,0px,0px;
             padding-top:0px;
             padding-bottom:0px;
         }
         QScrollBar::handle:vertical{
             width:3px;
             background:#4B4B4B;
             min-height:3;
         }
         QScrollBar::handle:vertical:hover{
             background:#3F3F3F;
             border:0px #3F3F3F;
         }
         QScrollBar::sub-line:vertical{
             width:0px;
             border-image:url(:/Res/scroll_left.png);
             subcontrol-position:left;
         }
         QScrollBar::sub-line:vertical:hover{
             height:0px;
             background:#222225;
             subcontrol-position:top;
         }
         QScrollBar::add-line:vertical{
             height:0px;
             border-image:url(:/Res/scroll_down.png);
             subcontrol-position:bottom;
         }
         QScrollBar::add-line:vertical:hover{
             height:0px;
             background:#3F3F3F;
             subcontrol-position:bottom;
         }
         QScrollBar::add-page:vertical{
             background:#2B2B2B;
         }
         QScrollBar::sub-page:vertical{
             background:#2B2B2B;
         }
         QScrollBar::up-arrow:vertical{
             border-style:outset;
             border-width:0px;
         }
         QScrollBar::down-arrow:vertical{
             border-style:outset;
             border-width:0px;
         }

         QScrollBar:horizontal{
             height:12px;
             border:1px #2B2B2B;
             margin:0px,0px,0px,0px;
             padding-left:0px;
             padding-right:0px;
         }
         QScrollBar::handle:horizontal{
             height:16px;
             background:#4B4B4B;
             min-width:20;
         }
         QScrollBar::handle:horizontal:hover{
             background:#3F3F3F;
             border:0px #3F3F3F;
         }
         QScrollBar::sub-line:horizontal{
             width:0px;
             border-image:url(:/Res/scroll_left.png);
             subcontrol-position:left;
         }
         QScrollBar::sub-line:horizontal:hover{
             width:0px;
             background:#2B2B2B;
             subcontrol-position:left;
         }
         QScrollBar::add-line:horizontal{
             width:0px;
             border-image:url(:/Res/scroll_right.png);
             subcontrol-position:right;
         }
         QScrollBar::add-line:horizontal:hover{
             width:0px;
             background::#2B2B2B;
             subcontrol-position:right;
         }
         QScrollBar::add-page:horizontal{
                    background:#2B2B2B;
         }
         QScrollBar::sub-page:horizontal{
                     background:#2B2B2B;
         }
        '''
        self.listWidget.setStyleSheet(self.scc)
        self.listWidget_2.setStyleSheet(self.scc)

        MainWindow.setWindowOpacity(0.95)  # 设置窗口透明度
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框



    def ten(self):
        num = self.lineEdit.text()
        print (num)
        num = int(num)
        if not num =='' and not num<=0 and not num>1000:
            if num > 20:
                reply = QtWidgets.QMessageBox.warning(self, u'警告', u'认真的吗，这么多？', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
            for i in range (0,int(num)):
                name = name_list[randint(0, len(name_list) - 1)]
                self.listWidget_2.addItem(name)
                self.listWidget.addItem(name)
        elif num =='':
            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'请输入数字', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
        elif num<0:
            #win32api.MessageBox(0, "你见过负数个人么???????", "通知", win32con.MB_OK | win32con.MB_ICONWARNING)
            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'你见过负数个人么???????', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
        elif num==0:
            #win32api.MessageBox(0, "人都被你吃了？？？", "通知", win32con.MB_OK | win32con.MB_ICONWARNING)
            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'人都被你吃了？？？', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
        elif num>100:
            #win32api.MessageBox(0, "抽这么多？想把老余也拉进来吗？~", "通知", win32con.MB_OK | win32con.MB_ICONWARNING)
            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'想玩？就不让你抽！！~', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()


    def cmxz(self):
        import webbrowser as web
        url = 'https://classone.top/ktdmq'
        web.open_new(url)

    def retranslateUi(self, MainWindow):
            self.wide = 420
            self.high = 360
            _translate = QtCore.QCoreApplication.translate
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.label.setText(_translate("MainWindow", "幸运儿是 {}"))
            self.label.setStyleSheet('color:white')
            self.pushButton.setText(_translate("MainWindow", "开始"))
            self.pushButton_2.setText(_translate("MainWindow", "结束"))
            self.label_2.setText(_translate("MainWindow", "点过的姓名："))
            self.pushButton_5.setText(_translate("MainWindow", "查看点过的名字"))
            self.pushButton_6.setText(_translate("MainWindow", "连抽模式"))
            self.label_3.setText(_translate("MainWindow", "连抽人数"))
            self.pushButton_7.setText(_translate("MainWindow", "开始"))
            self.pushButton_9.setText(_translate("MainWindow", "关于"))

    def showHistory(self):
        global seed
        if not seed:
            self.high = 705
            MainWindow.resize(self.wide,self.high)
            seed = True
            self.wide = 460
            MainWindow.resize(self.wide, self.high)
        else:
            self.high = 400
            MainWindow.resize(self.wide, self.high)
            seed = False
            self.wide = 460
            MainWindow.resize(self.wide, self.high)

    def showContinue(self):
        global choud
        if not choud:
            self.wide = 874
            MainWindow.resize(self.wide, self.high)
            choud = True
            self.high = 705
            MainWindow.resize(self.wide, self.high)
            seed = False
            
        else:
            self.wide = 460
            MainWindow.resize(self.wide, self.high)
            choud = False
            self.high = 400
            MainWindow.resize(self.wide, self.high)
            seed = False

    def gua(self):
        MessageBox(0, "就你也想开挂？？？", "~~~", MB_OK | MB_ICONWARNING)


    def setname(self):
        global running
        global name
        try:

            name = name_list[randint(0, len(name_list) - 1)]
            self.label.setText("恭喜 {}！".format(name))
            #print (running)
        except:
            self.name()
            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'发生错误，请检查name文件的学号后再重新打开本软件', QtWidgets.QMessageBox.Yes)
            sys.exit()

    def rename(self):
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'确定重置name文件?', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            with open('名单.txt', 'w') as f:
                print(f.truncate())
                print(f.write(a))
            MessageBox(0, "重置完成,", "通知", MB_OK | MB_ICONWARNING)
        else:
            pass

    def name(self):
        with open('名单.txt', 'w') as f:
            print(f.truncate())
            print(f.write(a))
        # win32api.MessageBox(0,"已将name文件重置，请及时修改","MessageBox",win32con.MB_OK | win32con.MB_ICONWARNING)

    def start(self):
        global running
        if running:
            print('running')
            pass
        else:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.setname)
            self.timer.start(50)
            running = 'True'

    def stop(self):
        global running, a
        if running:
            self.timer.stop()
            running = False
            self.listWidget.addItem(name)
        else:

            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'还没开始就想结束？', QtWidgets.QMessageBox.Yes)

    # 识别



# 重写MainWindow类
class MainWindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '提示',
                                               "是否要退出13班课堂点名器3.99 By Yish_？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        global big
        big = False

        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        global big
        big = False
        if Qt.LeftButton and self.m_flag:
            self.setWindowState(Qt.WindowNoState)
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global big
        big = False
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def big(self):
        global big
        print('最大化：{}'.format(big))
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        elif big:
            self.setWindowState(Qt.WindowNoState)
            big = False

    def close(self):
        reply = QtWidgets.QMessageBox.question(self, '提示',
                                               "是否要退出13班课堂点名器3.99 By Yish_？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass


    def mini(self):

        self.showMinimized()
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(645, 500)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(140, 100, 381, 291))
        self.label.setStyleSheet("yish.png);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()  # QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



