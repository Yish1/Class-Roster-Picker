关于
这个点名器源码来自Dragon少年 基于Python：pyqt5，我和QQB对其ui和bug进行了调整和修复。

可以每次单人抽取也可以自己选择连抽人数进行多人连抽，并将这些随机抽取的学生姓名历史数据显示，能够活跃课堂氛围，排除主观因素，真正做到随机点名。

但由于技术原因，在连续抽取模式下，暂时无法做到不重复。

制作：翰林实验学校2023届高三13班Yish_ (杨奕璇)2022.7.29于暑假期间

一起用Python做个上课点名器，好玩又实用！_Dragon少年的博客-CSDN博客_python点名器

课堂点名器 – QQB's Blog (hltool.top)

Yish1/ktdmq: 课堂点名器 (github.com)

----------------------------------------------

4.0版本发布说明 4.0Release Notes&Fixed Issues
1.修复高DPI模式下，字体不能完全展示的bug 由QQB修复

2.修复连抽模式下输入非数字导致崩溃的问题 由QQB修复

3.修复32位系统兼容性问题 由QQB修复

4.目前没有发现其他bug

5. 4.0版本稍后上传

6. 5.0版本或将完全重写界面，以后再说...

通用版本下载
https://yish.lanzouw.com/iWpvS09h32gd这是3.99

使用说明
名单：只有通用版本可以修改名单，打开后将自动在目录下生成名单.txt，您需要手动将里面的文字替换成点名的名单，格式为一行一个名字！！！

定制版本下载
定制版本名单封装至程序内，无法修改名单！！！

不再提供定制版下载，如有名单定制需求，可自行修改代码，或联系我。


----------------------------------------------

功能介绍
3.5使用视频

部分源码展示
    def ten(self):
        num = self.lineEdit.text()
        print (num)
        num = int(num)
        if not num =='' and not num<=0 and not num>43:
            if num > 20:
                reply = QtWidgets.QMessageBox.warning(self, u'警告', u'认真的吗，这么多', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
            for i in range (0,int(num)):
                name = name_list[randint(0, len(name_list) - 1)]
                self.listWidget_2.addItem(name)
                self.listWidget.addItem(name)
        elif num =='':
            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'请输入数字', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
        elif num<0:
            reply = QtWidgets.QMessageBox.warning(self, u'警告', u'你见过负数个人么???????', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
        elif num==0:
          reply = QtWidgets.QMessageBox.warning(self, u'警告', u'人都被你吃了？？？', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
        elif num>100:
 
            reply = QtWidgets.QMessageBox.warning(self, u'警告'想玩？就不让你抽！~', QtWidgets.QMessageBox.Yes)
            self.listWidget_2.clear()
 
    def ren(self):
        os.system('start ./名单.txt')
----------------------------------------------

Yish1/ktdmq: 课堂点名器 (github.com)

以下为过时的内容
2022.8.13更新3.99

此更新3.99仅限13班定制版点名器，其余版本仍为3.90-3.95（3.90到3.95内容完全一样）

①修复图标过于模糊的问题

②修复连抽区间在43-100内无效的问题

③优化UI间隙

2022.8.12更新 3.9

如果没有什么大问题，这将是最后一个版本！

①增大界面，增大字体，使文字能更好的在大屏幕上展示

②缓解了高DPI模式下无法完全显示文字的问题(还可以手动在电脑设置中将屏幕缩放比例调整至100%解决此问题)

③优化了连抽模式的体验

2022.7.29 更新3.0

①全新界面，新增连抽和历史记录

②真随机抽取

2022.6 2.0首个版本

----------------------------------------------

3.9版本中已知问题 Known Issues
①在连抽模式下无法做到不重复（涉及底层算法，因个人能力问题暂无法修复）

②屏幕DPI为125%时无法完全显示文字（已通过pyqt5开发文档中高DPI模式自适应代码修复，但似乎在部分设备上不起作用）

③当连抽输入为非数字时“”，int(num)将传递空信息导致崩溃，（修复失败...）

④不支持32位设备

⑤在连抽模式下，抽取人数在44-100区间内不会有提示，也无法抽取（因为我忘记改了，懒得修复，应该也不会抽这么多）

目前没有发现更多的问题。
