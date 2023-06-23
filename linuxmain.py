# -*- coding: utf-8 -*-
# 颜色可以是英文（white），或是#ffffff，UI的注释我写了出来！！
# ui美化：(line93:#任务栏的ico)(line427:#任务栏名称)
# 源码需要沉淀，下面的源码就是时间的沉淀

import sys, random, os, requests, ctypes, pygame
from os import path as pathq
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from datetime import datetime
import webbrowser as web
import matplotlib

matplotlib.use("QTAgg")
import matplotlib.pyplot as plt

dmversion = 5.1

# if not ctypes.windll.shell32.IsUserAnAdmin():
# result = MessageBox(0, "需要以管理员身份运行，是否继续？\n无管理员权限可能不能写入历史记录", "需要以管理员身份运行", MB_YESNO | MB_ICONWARNING)
# 调试时可以选择否
# if result == IDYES:
# ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
# sys.exit()新方法获取管理员权限，缺点是用户要每次手动确定

if sys.platform == "win32" and not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    # 在编辑器中请注释掉这句，否则不能运行调试，编译完后需要加上这句，否则打包后会启动两次点名器
    sys.exit()

big = False
running = False
seed = False
choud = False
zt = 50


def make_name_list():
    for i in range(1, 21):
        yield str(i).rjust(2, "0")


def init_name(name_list):
    with open("名单.txt", "w") as f:
        for i in name_list:
            print(f.write(i))
            f.write("\n")


name_list = []
mdcd = 0
pygame.init()
pygame.mixer.init()


def opentext(path):
    if sys.platform == "win32":
        os.system("start %s" % path)
    else:
        os.system("vim %s" % path)


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.RowLength = 0
        try:
            icon_path = pathq.join(pathq.dirname(__file__), "./yish.ico")  # 任务栏的ico
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path))
            MainWindow.setWindowIcon(icon)
        except:
            pass
        # self.setupUi(MainWindow())

    def setupUi(self, MainWindow):
        global name_list, mdcd
        try:
            with open("名单.txt", encoding="utf8") as f:
                # strip('\n')去掉字符串中的'\n'
                name_list = [line.strip("\n") for line in f.readlines()]
            print(name_list)
        except FileNotFoundError:
            name_list = list(make_name_list())
            init_name(name_list)
            QtWidgets.QMessageBox.information(
                self,
                "欢迎",
                "欢迎使用沉梦课堂点名器！ \n这是你第一次打开或者是名单被删除、移动。\n请及时修改目录下的名单文件，请确保格式正确（将原本的1-20的数字删除，一行输入一个名字，像下面这样）：\n小明\n小红\n小蓝\n需要帮助请点击关于。      \n 制作：Yish_ ，QQB，limuy2022   2022.7",
                QtWidgets.QMessageBox.Ok,
            )
            opentext("./名单.txt")
            print("读取到的有效名单长度 :", mdcd)
        mdcd = len(name_list)
        # 以下可直接粘贴生成的setupui代码
        MainWindow.setObjectName("沉梦课堂点名器")
        MainWindow.resize(460, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 45, 700, 150))  # 主体
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
        font.setFamily("宋体")
        self.listWidget.setFont(font)
        self.listWidget.setFocusPolicy(QtCore.Qt.WheelFocus)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 380, 210, 21))  # 文字
        self.label_2.setObjectName("label_2")
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.label_2.setFont(font)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(570, 646, 210, 30))  # 文字
        self.label_4.setObjectName("label_4")
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.label_4.setFont(font)

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(600, 10, 210, 30))  # 文字
        self.label_5.setObjectName("label_4")
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.label_5.setFont(font)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 320, 111, 35))  # 查看点过的名字
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(360, 320, 75, 35))  # 连抽模式
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(580, 370, 89, 20))  # 连抽输入框
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
        self.label_3.setGeometry(QtCore.QRect(525, 370, 56, 21))  # 连抽人数
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color:white;background:#323232")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(679, 360, 111, 40))  # 连抽开始
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 240, 100, 25))  # 修改名单按钮
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(690, 240, 100, 25))  # 历史记录按钮
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(550, 290, 100, 25))  # 统计按钮
        self.pushButton_8.setObjectName("pushButton_4")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(503, 420, 353, 221))  # 连抽列表
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
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )
        # 查看点过的名字
        self.pushButton_4.setStyleSheet(
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )
        # 查看历史记录
        self.pushButton_8.setStyleSheet(
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )
        # 查看历史记录
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
             color:#323232;
             background:#323232;
             border-top:1px solid #323232;
             border-bottom:1px solid #323232;
             border-right:1px solid #323232;
             border-left:1px solid #323232;
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
        self.pushButton_8.clicked.connect(self.countname)
        self.label_2.setStyleSheet("color:white")
        self.label_4.setStyleSheet("color:white")
        self.label_5.setStyleSheet("color:white")

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
             background:#323232;
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

        MainWindow.setWindowOpacity(0.98)  # 设置窗口透明度
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

    def retranslateUi(self, MainWindow):
        self.wide = 420
        self.high = 360
        _translate = QtCore.QCoreApplication.translate
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "沉梦课堂点名器%.1f") % dmversion
        )  # 任务栏名称
        self.label.setText(_translate("MainWindow", "幸运儿是 {}"))
        self.label.setStyleSheet("color:white")
        self.pushButton.setText(_translate("MainWindow", "开始"))
        self.pushButton_2.setText(_translate("MainWindow", "结束"))
        self.pushButton_3.setText(_translate("MainWindow", "修改名单文件"))
        self.pushButton_4.setText(_translate("MainWindow", "查看历史记录"))
        self.pushButton_8.setText(_translate("MainWindow", "统计中奖人员"))
        self.label_2.setText(_translate("MainWindow", "点过的姓名："))
        self.label_4.setText(
            _translate("MainWindow", "制作：Yish_，QQB，limuy2022  v%.1f") % dmversion
        )
        self.label_5.setText(_translate("MainWindow", "名单中共有:%s人") % mdcd)
        self.pushButton_5.setText(_translate("MainWindow", "查看点过的名字"))
        self.pushButton_6.setText(_translate("MainWindow", "连抽模式"))
        self.label_3.setText(_translate("MainWindow", "连抽人数"))
        self.pushButton_7.setText(_translate("MainWindow", "开始"))

        try:
            updatecheck = "https://classone.top/programs/dm/api/check.html"
            page = requests.get(updatecheck, verify=False, timeout=2)
            newversion = float(page.text)
            print("云端版本号为:", newversion)
            findnewversion = "检测到新版本！请点击左上角“更新”下载新版"
            if newversion > dmversion:  # if:条件
                print("检测到新版本:", newversion, "当前版本为:", dmversion)
                self.pushButton_9.setText(_translate("MainWindow", "更新"))
                self.wide = 460
                MainWindow.resize(self.wide, self.high)
                self.high = 705
                MainWindow.resize(self.wide, self.high)
                updatabutton = QMessageBox.question(
                    self,
                    "检测到新版本",
                    "云端最新版本为%s，要现在下载新版本吗？<br>您也可以稍后点击点名器左上角'更新'按钮升级新版本" % newversion,
                    QMessageBox.Ok | QMessageBox.No,
                    QMessageBox.Ok,
                )
                if updatabutton == QMessageBox.Ok:
                    web.open_new("https://classone.top/ktdmq")
                else:
                    pass
                self.listWidget.addItem(findnewversion)
            else:
                print("当前已经是最新版本:")
                self.pushButton_9.setText(_translate("MainWindow", "关于"))
        except:
            print("网络异常,无法检测更新")
            self.pushButton_9.setText(_translate("MainWindow", "关于"))
            noconnect = "网络连接异常，检查更新失败"
            self.listWidget.addItem(noconnect)

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
            self.listWidget_2.clear()
            name_set = set()
            while len(name_set) != num:
                name_set.add(random.choice(name_list))
            name_set = list(name_set)
            random.shuffle(name_set)
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                print(
                    today,
                    "沉梦课堂点名器%.1f" % dmversion,
                    "幸运儿是： %s " % name_set,
                    file=open("点名器中奖名单.txt", "a"),
                )
            except:
                print("无法写入历史记录")
            print(today, "幸运儿是： %s " % name_set)
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
                self,
                "警告",
                "你的名单中只有 %s 人 <br>连抽模式下不会重复抽取，请不要超过名单最大人数！" % lenth,
                QtWidgets.QMessageBox.Yes,
            )
            self.listWidget_2.clear()

    def cmxz(self):
        url = "https://classone.top/ktdmq"
        web.open_new(url)

    def ren(self):
        button = QMessageBox.question(
            self,
            "确定要修改名单？",
            "读取到名单中有 %s 人 <br> 接下来将关闭点名器确保名单能被正常修改，要继续吗？" % mdcd,
            QMessageBox.Ok | QMessageBox.No,
            QMessageBox.Ok,
        )
        if button == QMessageBox.Ok:
            opentext("./名单.txt")
            sys.exit()
        else:
            pass

    def dmhistory(self):
        opentext("./点名器中奖名单.txt")

    def countname(self):
        name_counts = {}  # 存储名字出现次数的字典
        with open("点名器中奖名单.txt") as file:
            for line in file:
                if "幸运儿是：" in line:
                    cnames = line.split("幸运儿是：")[1].strip().strip("[]'")
                    cnames = cnames.split("', '")
                    for cname in cnames:
                        if cname not in name_counts:
                            name_counts[cname] = 1
                        else:
                            name_counts[cname] += 1
        sorted_counts = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)
        names = [name for name, count in sorted_counts]
        counts = [count for name, count in sorted_counts]
        # 生成柱状图
        plt.rcParams["font.family"] = "Microsoft YaHei"
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(7680 / 300, 4320 / 300))
        bars = ax.bar(names, counts, color="cyan")
        ax.bar_label(bars, fmt="%d", fontsize=12)  # 在柱子上方标记数据
        ax.set_xlabel("名字")
        ax.set_ylabel("次数")
        ax.set_title("点名器中奖统计", fontsize=24)  # 设置标题字体大小
        ax.tick_params(axis="x", rotation=90)
        # 弹窗选择保存选项
        msg_box = QMessageBox()
        msg_box.setWindowTitle("保存选项")
        msg_box.setText("请选择保存方式")
        save_button = msg_box.addButton("保存为柱形图", QMessageBox.YesRole)
        cancel_button = msg_box.addButton("保存为文本", QMessageBox.NoRole)
        msg_box.setDefaultButton(cancel_button)
        msg_box.exec_()
        if msg_box.clickedButton() == save_button:
            # 保存图表
            plt.savefig("中奖统计图.png")
            QMessageBox.information(self, "保存结果", "图表已保存到'中奖统计图.png'")
            plt.show()
        elif msg_box.clickedButton() == cancel_button:
            # 保存文本
            cresult = "中奖名单统计(统计会覆盖上一次结果):\n"
            for name, count in sorted_counts:
                cresult += f"{name} 出现了 {count} 次\n"
            with open("中奖统计.txt", "w") as file:
                file.write(cresult)
            QMessageBox.information(self, "保存结果", "统计结果已保存到'中奖统计.txt'")
            opentext("./中奖统计.txt")

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
            # 定义文件夹的相对路径
            folder_name = "music"
            current_dir = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.join(current_dir, folder_name)
            if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
                print(f"音乐文件夹不存在或路径不正确：{folder_path}")
                os.makedirs(folder_path)  # 创建音乐文件夹
                return
            # 获取文件夹中的文件列表
            file_list = os.listdir(folder_path)
            if not file_list:
                print(f"要使用背景音乐功能，请在{folder_path}中放入mp3格式的音乐")
                return
            # 从列表中随机选择一个文件
            random_file = random.choice(file_list)
            # 生成完整的文件路径
            file_path = os.path.join(folder_path, random_file)
            try:
                print(f"播放音乐：{file_path}")
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except pygame.error as e:
                print(f"无法播放音乐文件：{file_path}，错误信息：{str(e)}")

    def stop(self):
        global running, a
        if running:
            self.timer.stop()
            running = False
            self.listWidget.addItem(name)
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                print(
                    today,
                    "沉梦课堂点名器%.1f" % dmversion,
                    "幸运儿是： %s " % name,
                    file=open("点名器中奖名单.txt", "a"),
                )
            except:
                print("无法写入历史记录")
            print(today, "幸运儿是： %s " % name)
            try:
                pygame.mixer.music.fadeout(1000)
            except pygame.error as e:
                print(f"停止音乐播放时发生错误：{str(e)}")

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
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()  # QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
