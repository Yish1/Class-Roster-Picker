# -*- coding: utf-8 -*-
# 颜色可以是英文（white），或是#ffffff，UI的注释我写了出来！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# ui美化：(line93:#任务栏的ico)(line427:#任务栏名称)
# 源码需要沉淀，下面的源码就是时间的沉淀

import sys, random,os
from os import path as pathq
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from win32api import MessageBox
from win32con import MB_OK, MB_ICONWARNING
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from datetime import datetime

dmversion = 4.6

# 屏幕检测
"""获取缩放后的分辨率"""
sX = win32api.GetSystemMetrics(0)  # 获得屏幕分辨率X轴
sY = win32api.GetSystemMetrics(1)  # 获得屏幕分辨率Y轴
"""获取真实的分辨率"""
hDC = win32gui.GetDC(0)
w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)  # 横向分辨率
h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)  # 纵向分辨率
# 缩放比率
screen_scale_rate = round(w / sX, 2)
dpi = screen_scale_rate
if dpi == 1.0:
    zt = 50
elif dpi == 1.25:
    zt = 40
elif dpi > 1.25:
    zt = 35
    MessageBox(0, "暂未适配当前分辨率或缩放模式，可尝试降低分辨率和缩放模式再打开，否则程序可能显示异常", "MessageBox", MB_OK | MB_ICONWARNING)

big = False
running = False
seed = False
choud = False

def make_name_list():
    for i in range(1, 21):
        yield str(i).rjust(2, '0')

def init_name(name_list):
    with open("名单.txt", "w") as f:
        for i in name_list:
            print(f.write(i))
            f.write('\n')


try:
    with open('名单.txt', encoding='utf8') as f:
        # strip('\n')去掉字符串中的'\n'
        name_list = [line.strip('\n') for line in f.readlines()]  
    print(name_list)
except FileNotFoundError:
    name_list = list(make_name_list())
    init_name(name_list)
    MessageBox(0, "欢迎使用沉梦课堂点名器！ \n这是你第一次打开或者是名单被删除、移动。\n请及时修改目录下的名单文件，请确保格式正确（将原本的1-20的数字删除，一行输入一个名字，像下面这样）：\n小明\n小红\n小蓝\n需要帮助请点击关于。      \n 制作：Yish_ ，QQB，limuy2022   2022.7", "MessageBox", MB_OK | MB_ICONWARNING)
    os.system('start ./名单.txt')

print ("读取到的有效名单长度 : ", len(name_list))

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.RowLength = 0
        try:
            icon_path = pathq.join(pathq.dirname(__file__), "./123.ico")  # 任务栏的ico
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path))  # 这是对的。
            MainWindow.setWindowIcon(icon)
        except:
            pass
        # self.setupUi(MainWindow())

    def setupUi(self, MainWindow):
        # 以下可直接粘贴生成的setupui代码
        MainWindow.setObjectName("沉梦课堂点名器")
        MainWindow.resize(460, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 45, 470, 150))  # 主体
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(zt)  # 主体大小#字体大小
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(75, 220, 111, 61))  # 开始按钮
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(283, 220, 111, 61))  # 结束按钮
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(20, 15, 50, 30))  # 关于
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(12, 420, 435, 250))  # 统计
        self.listWidget.setObjectName("listWidget")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.listWidget.setFont(font)
        self.listWidget.setFocusPolicy(QtCore.Qt.WheelFocus)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 380, 210, 21))  # 文字
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(570, 640, 210, 30))  # 文字
        self.label_4.setObjectName("label_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 320, 111, 35))  # 查看点过的名字
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(360, 320, 75, 35))  # 连抽模式
        self.pushButton_6.setObjectName("pushButton_6")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(580, 260, 89, 20))  # 连抽输入框
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("2")
        self.lineEdit.setStyleSheet(
            """
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
        
                """
        )
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(525, 260, 56, 21))  # 连抽人数
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color:white;background:#222225")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(679, 250, 111, 40))  # 连抽开始
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 600, 100, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(690, 600, 100, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(503, 20, 353, 221))  # 连抽列表
        font = QtGui.QFont()
        font.setPointSize(20)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.listWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget_2.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
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
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )  # 连抽开始
        self.pushButton_6.clicked.connect(self.showContinue)
        self.pushButton_7.clicked.connect(self.ten)
        self.pushButton_6.setStyleSheet(
            """QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}"""
        )  # 连抽模式
        self.pushButton.setStyleSheet(
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )  # 单抽开始
        self.pushButton_2.setStyleSheet(
            """QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}"""
        )  # 单抽停止
        self.pushButton_3.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
            #查看点过的名字
        self.pushButton_4.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
            #查看历史记录
        self.pushButton_9.setStyleSheet(
            """QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}"""
        )  # 关于
        # 以上可以修改
        self.pushButton_5.setStyleSheet(
            """QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}"""
        )  # 查看点过的名字
        # 以上可以修改
        self.centralwidget.setStyleSheet(
            """
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

             """
        )  # 上面是总（背景）
        self.close_widget = QtWidgets.QWidget(self.centralwidget)
        self.close_widget.setGeometry(QtCore.QRect(365, 5, 90, 30))
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
            """QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}"""
        )  # 右上角叉叉
        self.left_visit.setStyleSheet(
            """QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}"""
        )
        self.left_mini.setStyleSheet(
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )
        self.pushButton_9.clicked.connect(self.cmxz)
        self.pushButton_3.clicked.connect(self.ren)
        self.pushButton_4.clicked.connect(self.dmhistory)
        self.label_2.setStyleSheet("color:white")
        self.label_4.setStyleSheet("color:white")
 
        self.scc = """
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
        """
        self.listWidget.setStyleSheet(self.scc)
        self.listWidget_2.setStyleSheet(self.scc)

        MainWindow.setWindowOpacity(0.95)  # 设置窗口透明度
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
    def ten(self):
        lenth = len(name_list)
        num = self.lineEdit.text()
        print(num)
        try:
            num = int(num)
        except ValueError:
            reply = QtWidgets.QMessageBox.warning(
                self, "警告", "啥玩意呀？请输入数字!!!", QtWidgets.QMessageBox.Yes
            )
            return
        if not num <= 0 and not num > lenth:
            if num > lenth:
                reply = QtWidgets.QMessageBox.warning(
                    self, "警告", "连抽模式下名单不重复，请不要超过名单最大人数！", QtWidgets.QMessageBox.Yes
                )
            self.listWidget_2.clear()
            name_set = set()
            while len(name_set) != num:
                name_set.add(random.choice(name_list))
            name_set = list(name_set)
            random.shuffle(name_set)
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(today,"沉梦课堂点名器%.1f" %(dmversion) + ' : 幸运儿是： %s '  % name_set, file=open('点名器中奖名单.txt', 'a') )
            print(today,"幸运儿是： %s " % name_set)
            for name in name_set:
                self.listWidget_2.addItem(name)
                self.listWidget.addItem(name)
        elif num < 0:
            # win32api.MessageBox(0, "你见过负数个人么???????", "通知", win32con.MB_OK | win32con.MB_ICONWARNING)
            reply = QtWidgets.QMessageBox.warning(
                self, "警告", "你见过负数个人么???????", QtWidgets.QMessageBox.Yes
            )
            self.listWidget_2.clear()
        elif num == 0:
            # win32api.MessageBox(0, "人都被你吃了？？？", "通知", win32con.MB_OK | win32con.MB_ICONWARNING)
            reply = QtWidgets.QMessageBox.warning(
                self, "警告", "人都被你吃了？？？", QtWidgets.QMessageBox.Yes
            )
            self.listWidget_2.clear()
        elif num > lenth:
            # win32api.MessageBox(0, "想玩？就不让你抽！", "通知", win32con.MB_OK | win32con.MB_ICONWARNING)
            reply = QtWidgets.QMessageBox.warning(
                self, "警告", "超过名单最大人数！", QtWidgets.QMessageBox.Yes
            )
            self.listWidget_2.clear()

    def cmxz(self):
        import webbrowser as web

        url = "https://classone.top/ktdmq"
        web.open_new(url)

    def ren(self):
        MessageBox(0, "接下来将自动关闭点名器确保名单文件能被正常修改", "MessageBox", MB_OK | MB_ICONWARNING)
        os.system('start ./名单.txt')
        sys.exit()

    def dmhistory(self):
        os.system('start ./点名器中奖名单.txt')
        

    def retranslateUi(self, MainWindow):
        self.wide = 420
        self.high = 360
        _translate = QtCore.QCoreApplication.translate
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "沉梦课堂点名器%.1f")%dmversion)  # 任务栏名称
        self.label.setText(_translate("MainWindow", "幸运儿是 {}"))
        self.label.setStyleSheet("color:white")
        self.pushButton.setText(_translate("MainWindow", "开始"))
        self.pushButton_2.setText(_translate("MainWindow", "结束"))
        self.pushButton_3.setText(_translate("MainWindow", "修改名单文件"))
        self.pushButton_4.setText(_translate("MainWindow", "查看历史记录"))
        self.label_2.setText(_translate("MainWindow", "点过的姓名："))
        self.label_4.setText(_translate("MainWindow", "制作：Yish_，QQB，limuy2022  v%.1f") %dmversion)
        self.pushButton_5.setText(_translate("MainWindow", "查看点过的名字"))
        self.pushButton_6.setText(_translate("MainWindow", "连抽模式"))
        self.label_3.setText(_translate("MainWindow", "连抽人数"))
        self.pushButton_7.setText(_translate("MainWindow", "开始"))
        self.pushButton_9.setText(_translate("MainWindow", "关于"))

    def showHistory(self):
        global seed
        if not seed:
            self.high = 705
            MainWindow.resize(self.wide, self.high)
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
        global choud, seed
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
        global name
        if len(name_list) == 0:
            init_name(make_name_list())
            reply = QtWidgets.QMessageBox.warning(
                self, "警告", "名单文件为空，请输入名字（一行一个）后再重新打开本软件", QtWidgets.QMessageBox.Yes
            )
            sys.exit()
        name = random.choice(name_list)
        self.label.setText("恭喜 {}！".format(name))


    def rename(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "警告",
            "确定重置name文件?",
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            init_name(make_name_list())
            MessageBox(0, "重置完成,", "通知", MB_OK | MB_ICONWARNING)

    def start(self):
        global running
        if running:
            print("running")
            pass
        else:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.setname)
            self.timer.start(50)
            running = True

    def stop(self):
        global running, a
        if running:
            self.timer.stop()
            running = False
            self.listWidget.addItem(name)
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(today,"沉梦课堂点名器%.1f" %(dmversion) + ' : 幸运儿是： %s '  % name, file=open('点名器中奖名单.txt', 'a') )
            print(today,"幸运儿是： %s " % name)
        else:
            reply = QtWidgets.QMessageBox.warning(
                self, "警告", "还没开始就想结束？", QtWidgets.QMessageBox.Yes
            )


# 重写MainWindow类
class MainWindow(QtWidgets.QMainWindow):
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
        print("最大化：{}".format(big))
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        else:
            self.setWindowState(Qt.WindowNoState)
            big = False

    def close(self):
            sys.exit()

    def mini(self):
        self.showMinimized()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()  # QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
