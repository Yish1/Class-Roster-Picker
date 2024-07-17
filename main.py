# -*- coding: utf-8 -*-
import sys
import random
import difflib
import os
import requests
import pygame
import hashlib
import gettext
import glob
import ctypes
import win32com.client
#import ptvsd  # QThread断点工具
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QDesktopWidget, QMessageBox, QListView, QMainWindow, QGridLayout, QInputDialog
from datetime import datetime, timedelta
from Crypto.Cipher import ARC4
import webbrowser as web

try:
    with open('language.ini', 'r') as file:
        language_value = str(file.read())
    localedir1 = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'locale')
    translate = gettext.translation(
        domain=f"{language_value}", localedir=localedir1, languages=[f"{language_value}"])
    _ = translate.gettext
except:
    localedir1 = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'locale')
    translate = gettext.translation(
        domain="zh_CN", localedir=localedir1, languages=["zh_CN"])
    _ = translate.gettext

dmversion = 5.96

big = False
running = False
seed = False
choud = False

zt = 50
name_list = []
default_name_list = _("默认名单")
file_path = f"name/{default_name_list}.txt"
selected_file = f"{default_name_list}"
is_first_run = "0"
mdcd = 0
pygame.init()
pygame.mixer.init()


def make_name_list():
    for i in range(1, 21):
        yield str(i).rjust(2, "0")


def init_name(name_list):
    global name_path
    name_path = os.path.join("name", f"{default_name_list}.txt")  # 打开文件并写入内容
    with open(name_path, "w", encoding="utf8") as f:
        for i in name_list:
            f.write(i)
            f.write("\n")


def opentext(path):
    if sys.platform == "win32":
        os.system("start %s" % path)
    else:
        os.system("vim %s" % path)


def ttsinitialize():
    global allownametts
    try:
        with open('allownametts.ini', 'r') as file:
            allownametts = int(file.read())
    except FileNotFoundError:
        # 语音播报开关
        ifvoice = QMessageBox()
        ifvoice.setWindowTitle(_("语音播报"))
        ifvoice.setText(_(
            "需要开启语音播报功能吗？\n单抽后会播报抽取结果。\n"))
        allow_button = ifvoice.addButton(_("好的"), QMessageBox.ActionRole)
        cancel_button = ifvoice.addButton(_("下次一定"), QMessageBox.ActionRole)
        dictation_button = ifvoice.addButton(
            _("听写模式(不会读\"恭喜\")"), QMessageBox.ActionRole)
        button = ifvoice.addButton(_("取消"), QMessageBox.NoRole)
        button.setVisible(False)
        ifvoice.exec_()
        if ifvoice.clickedButton() == allow_button:
            # 同意
            allownametts = 1
            with open('allownametts.ini', "w", encoding='utf-8') as f:
                f.write("1")
            QMessageBox.information(
                None, _("语音播报"), _("语音播报已经开启，您可以删除目录下的allownametts.ini重新设置此功能。"))
        elif ifvoice.clickedButton() == cancel_button:
            allownametts = 0
            # 不同意
            with open('allownametts.ini', "w", encoding='utf-8') as f:
                f.write("0")
            QMessageBox.information(
                None, _("语音播报"), _("语音播报已禁用，您可以删除目录下的allownametts.ini重新设置此功能。"))
        elif ifvoice.clickedButton() == dictation_button:
            allownametts = 2
            # 听写模式
            with open('allownametts.ini', "w", encoding='utf-8') as f:
                f.write("2")
            QMessageBox.information(
                None, _("语音播报"), _("语音播报（听写模式）已启用，您可以删除目录下的allownametts.ini重新设置此功能。"))
    except ValueError:
        QMessageBox.information(
            None, _("语音播报"), _("目录下的allownametts.ini中不是一个有效的值"))
        if os.path.exists("allownametts.ini"):
            os.remove("allownametts.ini")
            ttsinitialize()


def ttsread(text):
    global allownametts
    if allownametts == 1:
        print(_("语音播报已开启"))
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
    elif allownametts == 2:
        print(_("语音播报（听写模式）已开启"))
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
    else:
        allownametts == 0
        print(_("语音播报已关闭"))


def first_run():
    global is_first_run
    init_name(make_name_list())
    app = QApplication(sys.argv)
    welcom = QMessageBox()
    welcom.setWindowTitle(_("欢迎使用"))
    welcom.setText(_("欢迎使用沉梦课堂点名器！\n本程序支持单抽，连抽。同时提供单抽时背景音乐、多名单支持、数据导出等功能。\n\n请及时修改目录下的名单文件，请确保格式正确（将原本的1-20的数字删除，一行输入一个名字，像下面这样）：\n名字1\n名字2\n名字3\n名字4\n名字5\n名字6\n......\n\n请在名单管理器中处理好名单，下次运行将开启名单校验功能。\n\n如需帮助请点击关于按钮。\n\n沉梦小站"))
    # 设置消息框的图标和按钮
    welcom.setIconPixmap(QIcon('picker.ico').pixmap(64, 64))  # 64x64 大小的图标
    welcom.setStandardButtons(QMessageBox.Ok)
    welcom.exec_()
    is_first_run = '1'
    opentext(name_path)
    print(_("这应该是首次启动"))
    return


def name_list_selector():
    global txtnum, name_list, file_path, namefolder, mdnum, is_first_run
    try:
        with open('allownameselect.ini', 'r') as file:
            allownameselect_value = int(file.read())
            if allownameselect_value == 1:
                select = 1
                print(_("已配置为名单数量大于1时显示选择窗口"))
            else:
                select = 0
                print(_("配置文件仅支持0或1，0或其他数字默认为0"))
    except:
        allownameselect_value = 0
        print(_("名单管理器配置文件错误或不存在，默认名单数量大于0时显示选择窗口"))
        select = 0
    namefolder = "name"
    os.makedirs("name", exist_ok=True)
    if not os.path.exists(namefolder) or not os.listdir(namefolder):
        first_run()
    txtnum = [filename for filename in os.listdir(
        namefolder) if filename.endswith(".txt")]
    mdnum = len(txtnum)
    if mdnum > select:
        # 创建窗口和UI元素
        app1 = QApplication([])
        window = QWidget()
        window.setWindowTitle(_('名单管理'))
        window.setGeometry(100, 100, 500, 200)
        layout = QVBoxLayout()
        combo_box = QComboBox(window)
        custom_list_view = QListView(combo_box)
        combo_box.setFixedHeight(40)
        custom_list_view.setStyleSheet("QListView::item { height: 40px; }")
        combo_box.setView(custom_list_view)
        layout.addWidget(combo_box)
        button = QPushButton(_('确定'), window)
        button.setFixedHeight(40)
        layout.addWidget(button)
        window.setLayout(layout)
        screen = QDesktopWidget().screenGeometry()
        window_width, window_height = window.sizeHint().width(), window.sizeHint().height()
        x = int((screen.width() - window_width) // 2.25)
        y = int((screen.height() - window_height) // 2.25)
        window.setGeometry(x, y, 500, 200)
        layout.addStretch()
        layout.addSpacing(40)
        add_button = QPushButton(_('新增名单'), window)
        add_button.setFixedHeight(40)
        layout.addWidget(add_button)
        delete_button = QPushButton(_('删除名单'), window)
        delete_button.setFixedHeight(40)
        layout.addWidget(delete_button)
        change_button = QPushButton(_('修改名单'), window)
        change_button.setFixedHeight(40)
        layout.addWidget(change_button)

        def add_new_list():
            newfilename, ok_pressed = QInputDialog.getText(
                window, _("新增名单"), _("请输入名单名称:(文件名即可，无需输入.txt)"))
            if ok_pressed and newfilename:
                print("新增名单名称是: {newfilename}")
                newnamepath = os.path.join(
                    "name", f"{newfilename}.txt")  # 打开文件并写入内容
                with open(newnamepath, "w", encoding="utf8") as f:
                    pass
                message = (_("已创建名为 '%s.txt' 的文件，路径为: %s") %
                           (newfilename, newnamepath))

                QMessageBox.information(
                    window, _("新建成功"), message, QMessageBox.Ok)
                opentext(newnamepath)
                txtnum = [filename for filename in os.listdir(
                    "name") if filename.endswith(".txt")]
                combo_box.clear()  # 清空下拉框的选项
                combo_box.addItems(txtnum)  # 添加新的文件名到下拉框
        add_button.clicked.connect(add_new_list)

        def delete_list():
            target_filename, ok_pressed = QInputDialog.getText(
                window, _("删除名单"), _("请输入要删除的名单名称:(文件名即可，无需输入.txt)"))
            if ok_pressed and target_filename:
                target_filepath = os.path.join(
                    "name", f"{target_filename}.txt")
                if os.path.exists(target_filepath):
                    os.remove(target_filepath)  # 删除文件
                    message = (_("已成功删除名为 '%s.txt' 的文件。") % target_filename)
                    QMessageBox.information(
                        window, _("删除成功"), message, QMessageBox.Ok)
                    txtnum = [filename for filename in os.listdir(
                        "name") if filename.endswith(".txt")]
                    combo_box.clear()  # 清空下拉框的选项
                    combo_box.addItems(txtnum)  # 添加新的文件名到下拉框
                else:
                    QMessageBox.warning(
                        window, _('警告'), _('名单文件不存在'), QMessageBox.Ok)
        delete_button.clicked.connect(delete_list)

        def change_name_list():
            target_filename = combo_box.currentText()
            target_filepath = os.path.join(
                    "name", f"{target_filename}")
            if os.path.exists(target_filepath):
                opentext(target_filepath)
            else:
                QMessageBox.warning(
                    window, _('警告'), _('名单文件不存在'), QMessageBox.Ok)
        change_button.clicked.connect(change_name_list)
        combo_box.addItems(txtnum)

        def showlist():
            global selected_file, file_path
            selected_file = combo_box.currentText()
            file_path = os.path.join("name", selected_file)
            if not os.path.exists(file_path):
                QMessageBox.warning(window, _('警告'), _(
                    '名单文件不存在'), QMessageBox.Ok)
            else:
                print(f"所选文件的路径为: {file_path}\n")
                window.close()
        button.clicked.connect(showlist)
        # 显示窗口
        window.show()
        app1.exec_()
    else:
        pass


def cs_sha256():
    delrecordfile = 0
    app = QApplication([])
    os.makedirs('data', exist_ok=True)
    ctypes.windll.kernel32.SetFileAttributesW('data', 2)
    os.makedirs('bak', exist_ok=True)
    ctypes.windll.kernel32.SetFileAttributesW('bak', 2)

    for filename1 in os.listdir('name'):
        if filename1.endswith('.txt'):
            file_path = os.path.join('name', filename1)
            output_file_path = os.path.join('data', filename1 + '.cmxz')

            if not os.path.exists(output_file_path):
                sha256_value = calculate_sha256(file_path)
                with open(output_file_path, 'w') as f:
                    f.write(sha256_value)
                print(f'已保存标识符值：{output_file_path}')
                fileoperation('name', filename1, 'encrypt')
            else:
                sha256_value = calculate_sha256(file_path)
                with open(output_file_path, 'r') as f:
                    saved_sha256_value = f.read().strip()

                if sha256_value == saved_sha256_value:
                    print(f'{filename1} 的标识符值与记录一致。')
                    fileoperation('name', filename1, 'encrypt')

                else:
                    print(f'警告：{filename1} 的标识符值与记录不一致。')
                    fileoperation('bak', filename1, 'decrypt')
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as original_file, open(processed_file_path, 'r', encoding='utf-8', errors='ignore') as bak_file:
                        original_content = original_file.read()
                        bak_content = bak_file.read()

                        if original_content == bak_content:
                            print(_('文件内容一致。'))
                        else:
                            print(_('文件内容不一致。以下是修改的内容：'))
                            # 去除内容中的空行
                            bak_lines = [line for line in bak_content.splitlines() if line.strip()]
                            original_lines = [line for line in original_content.splitlines() if line.strip()]
                            diff = difflib.unified_diff(bak_lines, original_lines)
                            diff_str = '\n'.join(diff)
                            diff_str = diff_str[11:]
                            msg_box = QMessageBox()
                            msg_box.setIcon(QMessageBox.Warning)
                            msg_box.setWindowTitle(_("警告"))
                            msg_box.setText(
                                _('警告：%s 最近被修改，加号是新增的，减号是减少的\n\n此记录会在 2天后 不再展示。\n%s') % (filename1, diff_str))
                            msg_box.exec_()
                            # 确保在最后一次循环才执行manage_deadline(filename1)
                            delrecordfile = delrecordfile + 1

    if delrecordfile > 0:
        manage_deadline("0")


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def fileoperation(folder_path, filename, operation):
    enfilename = filename + ".cmxz"
    file_path = os.path.join(folder_path, filename)
    if operation == 'encrypt':
        if filename.endswith('.txt'):
            process_file(file_path, 'encrypt')
    elif operation == 'decrypt':
        if enfilename.endswith('.cmxz'):
            file_path = os.path.join(folder_path, enfilename)
            process_file(file_path, 'decrypt')
        return processed_file_path


def process_file(file_path, operation):
    global processed_file_path
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        # 文件不存在时弹窗提示
        bpp = QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(_("警告"))
        msg_box.setText(_('警告：%s 的备份被删除，此名单可能已经被修改！') % file_path)
        msg_box.exec_()
    cipher = ARC4.new(b'cmxztopktdmq')
    if operation == 'encrypt':
        try:
            processed_data = cipher.encrypt(data)
            processed_file_path = os.path.join(
                'bak', os.path.basename(file_path) + '.cmxz')
            if os.path.exists(processed_file_path):
                print(f'加密文件已存在: {processed_file_path}')
                return processed_file_path
        except:
            print(_("加密文件不存在"))

    elif operation == 'decrypt':
        try:
            processed_data = cipher.decrypt(data)
            original_filename = os.path.basename(file_path)[:-5]
            processed_file_path = os.path.join('bak', original_filename)
        except:
            print(_("解密文件不存在"))

    try:
        with open(processed_file_path, 'wb') as f:
            f.write(processed_data)

        print(f'文件{operation}成功: {processed_file_path}')
        return processed_file_path
    except:
        manage_deadline("1")


def manage_deadline(now):
    timefile_path = os.path.join('bak', 'adeadline.txt')
    current_date = datetime.now().date()

    def write_to_file():
        # 获取默认截止日期并写入文件
        global result_time
        deadline_date = datetime.now() + timedelta(days=2)
        result_time = deadline_date
        if now != "1":
            with open(timefile_path, 'w') as file:
                file.write(deadline_date.strftime('%Y-%m-%d'))
            fileoperation('bak', 'adeadline.txt', 'encrypt')
            os.remove(timefile_path)
        else:
            print(_("名单校验已重置"))

    def read_from_file():
        # 从文件中读取截止日期
        if os.path.exists(timefile_path + '.cmxz'):
            fileoperation('bak', 'adeadline.txt', 'decrypt')
            with open(timefile_path, 'r') as file:
                date_str = file.read().strip()
                if date_str:
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
            return None

    def remove_directory(data_folder):
        txt_files = glob.glob(os.path.join(data_folder, '*.txt'))
        # 获取指定文件夹中所有扩展名为 .cmxz 的文件列表
        cmxz_files = glob.glob(os.path.join(data_folder, '*.cmxz'))
        all_files = txt_files + cmxz_files
        # 循环删除文件
        for file_path in all_files:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}")

    deadline_date = read_from_file()

    if deadline_date:
        # 如果截止日期已过，删除数据文件夹
        if current_date > deadline_date:
            print(f"截止日期({deadline_date})已过。删除数据文件夹。")
            try:
                # 递归删除目录及其内容
                remove_directory("data")
                remove_directory("bak")
                print(_("数据文件夹已删除。"))
            except OSError as e:
                print(f"删除数据文件夹时发生错误: {e}")
        else:
            print(f"截止日期是{deadline_date}。尚未过期。暂不重置校验")
            if now == "1":
                remove_directory("data")  # 异常处理
                remove_directory("bak")
            try:
                os.remove(timefile_path)
            except:
                pass
    else:
        # 如果没有截止日期，生成随机日期并写入文件
        if now == "1":
            remove_directory("data")  # 异常处理
            remove_directory("bak")
        write_to_file()
        print(f"生成了一个随机截止日期: {result_time}。写入文件。")


class Ui_MainWindow(QMainWindow):
    def init(self):
        super().init()
        self.RowLength = 0
        try:
            icon_path = os.path.join(os.path.dirname(
                __file__), "./picker.ico")  # 任务栏的ico
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path))
            MainWindow.setWindowIcon(icon)
        except:
            pass
        # self.setupUi(MainWindow())

    def setupUi(self, MainWindow):
        global mdcd, name_list, file_path
        if not os.path.exists(file_path):
            sys.exit()
        with open(file_path, encoding='utf8') as f:
            name_list = [line.strip('\n') for line in f.readlines()]
        print("\n", name_list)
        mdcd = len(name_list)
        print(_("读取到的有效名单长度 :"), mdcd)
        # 以下可直接粘贴生成的setupui代码
        MainWindow.setObjectName(_("沉梦课堂点名器"))
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
        self.label_4.setGeometry(QtCore.QRect(570, 10, 210, 30))  # 文字
        self.label_4.setObjectName("label_4")
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.label_4.setFont(font)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(
            QtCore.QRect(20, 320, 111, 35))  # 查看点过的名字
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
        self.lineEdit.setGeometry(QtCore.QRect(600, 370, 89, 20))  # 连抽输入框
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
        self.label_3.setGeometry(QtCore.QRect(525, 370, 60, 21))  # 连抽人数
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color:white;background:#323232")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(710, 360, 111, 40))  # 连抽开始
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(
            QtCore.QRect(550, 240, 100, 25))  # 修改名单按钮
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(
            QtCore.QRect(690, 215, 100, 25))  # 历史记录按钮
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(550, 290, 100, 25))  # 统计按钮
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(
            QtCore.QRect(690, 265, 100, 25))  # 背景音乐按钮
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(550, 190, 100, 25))  # 应用中心
        self.pushButton_11.setObjectName("pushButton_11")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(503, 420, 358, 250))  # 连抽列表
        font = QtGui.QFont()
        font.setPointSize(20)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.listWidget_2.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget_2.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
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
        # 统计名单
        self.pushButton_9.setStyleSheet(
            """QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}"""
        )  # 关于
        self.pushButton_10.setStyleSheet(
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )
        # 统计名单
        self.pushButton_11.setStyleSheet(
            """QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}"""
        )  # 应用中心
        self.pushButton_5.setStyleSheet(
            """QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}"""
        )  # 查看点过的名字
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

        self.left_close = QPushButton("×")  # 关闭按钮
        self.left_close.clicked.connect(MainWindow.close)
        self.left_visit = QPushButton("□")  # 最大化按钮
        self.left_visit.clicked.connect(MainWindow.big)
        self.left_mini = QPushButton("-")  # 最小化按钮
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
        self.pushButton_10.clicked.connect(self.bgmusic)
        self.pushButton_11.clicked.connect(self.moreprogram)
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
        MainWindow.setWindowTitle(_translate(
            "MainWindow", _("沉梦课堂点名器%.1f")) % dmversion)  # 任务栏名称
        self.label.setText(_translate("MainWindow", _("幸运儿是 {}")))
        self.label.setStyleSheet("color:white")
        self.pushButton.setText(_translate("MainWindow", _("开始")))
        self.pushButton_9.setText(_translate("MainWindow", _("关于")))
        self.pushButton_2.setText(_translate("MainWindow", _("结束")))
        self.pushButton_3.setText(_translate("MainWindow", _("修改名单文件")))
        self.pushButton_4.setText(_translate("MainWindow", _("查看历史记录")))
        self.pushButton_8.setText(_translate("MainWindow", _("统计中奖人员")))
        self.pushButton_10.setText(_translate("MainWindow", _("背景音乐目录")))
        self.pushButton_11.setText(_translate("MainWindow", _("获取更多应用")))
        self.label_2.setText(_translate("MainWindow", _("点过的姓名：")))
        self.label_4.setText(_translate(
            "MainWindow", "制作：Yish_，QQB，limuy2022  v%.1f") % dmversion)
        self.pushButton_5.setText(_translate("MainWindow", _("查看点过的名字")))
        self.pushButton_6.setText(_translate("MainWindow", _("连抽模式")))
        self.label_3.setText(_translate("MainWindow", _("连抽人数")))
        self.pushButton_7.setText(_translate("MainWindow", _("开始")))
        self.listWidget.addItem(_("选择了%s,共有:%s人") % (selected_file, mdcd))

        try:
            with open('allowcheck.ini', 'r') as file:
                allowcheck_value = int(file.read())
                if allowcheck_value == 1:
                    try:
                        updatecheck = "https://cdn.cmxz.top/programs/dm/api/check.html"
                        page = requests.get(updatecheck, timeout=1.5)
                        newversion = float(page.text)
                        print("云端版本号为:", newversion)
                        findnewversion = _("检测到新版本！请点击左上角“更新”下载新版")
                        if newversion > dmversion:
                            print(_("检测到新版本:"), newversion,
                                  _("当前版本为:"), dmversion)
                            self.pushButton_9.setText(
                                _translate("MainWindow", _("更新")))
                            updatabutton = QMessageBox.question(self, _("检测到新版本"), _("云端最新版本为%s，要现在下载新版本吗？<br>您也可以稍后点击点名器左上角'更新'按钮升级新版本") % newversion,
                                                                QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok,)
                            if updatabutton == QMessageBox.Ok:
                                web.open_new("https://cmxz.top/ktdmq")
                            else:
                                pass
                                self.listWidget.addItem(findnewversion)
                        else:
                            print(_("当前已经是最新版本:"))
                    except:
                        print(_("网络异常,无法检测更新"))
                        noconnect = _("网络连接异常，检查更新失败")
                        self.listWidget.addItem(noconnect)

                elif allowcheck_value == 0:
                    print(_("检查更新已关闭"))

        except FileNotFoundError:
            # 检查更新开关
            ifupdate = QMessageBox()
            ifupdate.setWindowTitle(_("检查更新"))
            ifupdate.setText(
                _("需要开启检查更新功能吗？\n新版本会带来新功能、优化以及修复错误。\n在服务器发布新版本后，会在您打开点名器时收到更新的提示"))
            allow_button = ifupdate.addButton(
                _("好的，谢谢你"), QMessageBox.ActionRole)
            cancel_button = ifupdate.addButton(
                _("下次一定"), QMessageBox.ActionRole)
            button = ifupdate.addButton(_("取消"), QMessageBox.NoRole)
            button.setVisible(False)
            ifupdate.exec_()
            if ifupdate.clickedButton() == allow_button:
                # 同意
                print(_("检查更新已开启"))
                with open('allowcheck.ini', "w", encoding='utf-8') as f:
                    f.write("1")
                QMessageBox.information(
                    self, _("检查更新"), _("检查更新功能已经开启，您可以删除目录下的allowcheck.ini重新设置此功能。"))
            elif ifupdate.clickedButton() == cancel_button:
                # 不同意
                with open('allowcheck.ini', "w", encoding='utf-8') as f:
                    f.write("0")
                ifupdate1 = QMessageBox()
                ifupdate1.setWindowTitle(_("真的不需要吗（π一π）"))
                ifupdate1.setText(
                    _("我们的每一次的更新都是很有意义的，能给您带来更好的体验，真的不开启检查更新功能吗？\no(╥﹏╥)o\no(╥﹏╥)o\no(╥﹏╥)o"))
                allow_button1 = ifupdate1.addButton(
                    _("行吧，我准许了"), QMessageBox.ActionRole)
                allow_button2 = ifupdate1.addButton(
                    _("算了，我同意了"), QMessageBox.ActionRole)
                cancel_button1 = ifupdate1.addButton(
                    _("不要，我不要啊"), QMessageBox.ActionRole)
                allow_button3 = ifupdate1.addButton(
                    _("行了，快开启吧"), QMessageBox.ActionRole)
                button1 = ifupdate1.addButton(_("取消"), QMessageBox.NoRole)
                button1.setVisible(False)
                ifupdate1.exec_()
                if ifupdate1.clickedButton() == allow_button1 or ifupdate1.clickedButton() == allow_button2 or ifupdate1.clickedButton() == allow_button3:
                    # 梅开二度
                    print(_("检查更新已开启"))
                    with open('allowcheck.ini', "w", encoding='utf-8') as f:
                        f.write("1")
                    QMessageBox.information(
                        self, _("检查更新"), _("检查更新功能已经开启，您可以删除目录下的allowcheck.ini重新设置此功能。"))
                else:
                    pass
        except ValueError:
            QMessageBox.information(
                self, _("检查更新"), _("目录下的allowcheck.ini中不是一个有效的值"))
            if os.path.exists("allowcheck.ini"):
                os.remove("allowcheck.ini")

    def ten(self):
        lenth = len(name_list)
        num = self.lineEdit.text()
        print(num)
        try:
            num = int(num)
        except ValueError:
            reply = QtWidgets.QMessageBox.warning(
                self, _("警告"), _("啥玩意呀？请输入数字!!!"), QtWidgets.QMessageBox.Yes
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
                    _("沉梦课堂点名器%.1f") % dmversion,
                    "幸运儿是： %s " % name_set,
                    file=open(_("点名器中奖名单.txt"), "a"),
                )
            except:
                print(_("无法写入历史记录"))
            print(today, "幸运儿是： %s " % name_set)
            for name in name_set:
                self.listWidget_2.addItem(name)
                self.listWidget.addItem(name)
        elif num < 0:
            reply = QtWidgets.QMessageBox.warning(
                self, _("警告"), _("你见过负数个人么???????"), QtWidgets.QMessageBox.Yes
            )
            self.listWidget_2.clear()
        elif num == 0:
            reply = QtWidgets.QMessageBox.warning(
                self, _("警告"), _("人都被你吃了？？？"), QtWidgets.QMessageBox.Yes
            )
            self.listWidget_2.clear()
        elif num > lenth:
            reply = QtWidgets.QMessageBox.warning(
                self,
                _("警告"),
                _("你的名单中只有 %s 人 <br>连抽模式下不会重复抽取，请不要超过名单最大人数！") % lenth,
                QtWidgets.QMessageBox.Yes,
            )
            self.listWidget_2.clear()

    def cmxz(self):
        url = "https://cmxz.top/ktdmq"
        web.open_new(url)

    def ren(self):
        button = QMessageBox.question(
            self,
            _("确定要修改名单？"),
            _("读取到名单中有 %s 人 <br> 接下来将关闭点名器确保名单能被正常修改，名单修改后会触发名单校验功能，名单被修改的部分将会被展示两天，要继续吗？<br>在打开的文件中输入名字，一行一个") % mdcd,
            QMessageBox.Ok | QMessageBox.No,
            QMessageBox.Ok,
        )
        if button == QMessageBox.Ok:
            opentext(file_path)
            sys.exit()
        else:
            pass

    def dmhistory(self):
        opentext(_("./点名器中奖名单.txt"))

    def bgmusic(self):
        QMessageBox.information(
            self, _("背景音乐"), _("若要使用背景音乐功能，请在稍后打开的文件夹中放入mp3格式的背景音乐 \n删除文件夹中的音乐则关闭此功能"))
        os.makedirs('dmmusic', exist_ok=True)
        opentext("dmmusic")

    def countname(self):
        name_counts = {}  # 存储名字出现次数的字典
        with open(_("点名器中奖名单.txt")) as file:
            for line in file:
                if "幸运儿是：" in line:
                    cnames = line.split("幸运儿是：")[1].strip().strip("[]'")
                    cnames = cnames.split("', '")
                    for cname in cnames:
                        if cname not in name_counts:
                            name_counts[cname] = 1
                        else:
                            name_counts[cname] += 1
        sorted_counts = sorted(name_counts.items(),
                               key=lambda x: x[1], reverse=True)
        # 保存文本
        print(_("正在保存为文本"))
        cresult = _("中奖名单统计(统计会覆盖上一次结果):\n")
        for name, count in sorted_counts:
            cresult += _("%s 出现了 %s 次\n") % (name, count)
            with open('中奖统计.txt', 'w') as file:
                file.write(cresult)
        QMessageBox.information(self, _("保存结果"), _("统计结果已保存到'中奖统计.txt'"))
        opentext('中奖统计.txt')

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
                self, _("警告"), _(
                    "名单文件为空，请输入名字（一行一个）后再重新打开本软件"), QtWidgets.QMessageBox.Yes
            )
            sys.exit()
        name = random.choice(name_list)
        self.label.setText(_("🎉 {}！").format(name))

    def start(self):
        global running
        if running:
            print("running")
            pass
        else:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.setname)
            self.timer.start(15)
            running = True
            folder_name = "dmmusic"
            current_dir = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.join(current_dir, folder_name)
            os.makedirs('dmmusic', exist_ok=True)
            # 获取文件夹中的文件列表
            file_list = os.listdir(folder_path)
            if not file_list:
                print(_("要使用背景音乐功能，请在 %s 中放入mp3格式的音乐") % folder_path)
                return
            # 从列表中随机选择一个文件
            random_file = random.choice(file_list)
            # 生成完整的文件路径
            file_path = os.path.join(folder_path, random_file)
            try:
                print(_("播放音乐：%s") % file_path)
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except pygame.error as e:
                print(_("无法播放音乐文件：%s，错误信息：{str(e)}") % file_path)

    def stop(self):
        global running, allownametts
        if running:
            self.timer.stop()
            running = False
            self.listWidget.addItem(name)
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                print(
                    today,
                    _("沉梦课堂点名器%.1f") % dmversion,
                    "幸运儿是： %s " % name,
                    file=open("点名器中奖名单.txt", "a"),
                )
            except:
                print(_("无法写入历史记录"))
            print(today, "幸运儿是： %s " % name)
            try:
                pygame.mixer.music.fadeout(800)
            except pygame.error as e:
                print(f"停止音乐播放时发生错误：{str(e)}")
            ttsinitialize()
            if allownametts == 1:
                ttsread(text=_("恭喜 %s") % name)
            elif allownametts == 2:
                ttsread(text=name)
            elif allownametts == 0:
                pass
            else:
                if os.path.exists("allownametts.ini"):
                    os.remove("allownametts.ini")
                ttsinitialize()
        else:
            reply = QtWidgets.QMessageBox.warning(
                self, _("警告"), _("还没开始就想结束？"), QtWidgets.QMessageBox.Yes
            )

    def moreprogram(self):
        url = "https://cmxz.top/downloads"
        web.open_new(url)


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
        print("最大化：{}").format(big)
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
    if is_first_run != "1":
        name_list_selector()
        cs_sha256()
    elif is_first_run == "1":
        first_run()
        name_list_selector()
    else:
        pass
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()  # QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
