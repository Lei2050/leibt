from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QTabWidget
from PyQt6.QtWidgets import QHBoxLayout, QListWidget, QStackedWidget, QDockWidget, QLabel, QScrollBar
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QObject, Qt, pyqtSignal
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级控件-QTabWidget容器控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        self.tab = QTabWidget(self)
        self.tab.resize(500, 400)
        # 创建三个窗口控件
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # 添加窗口到QTabWidget容器控件
        self.tab.addTab(self.tab1, '窗口一')
        self.tab.addTab(self.tab2, '窗口二')
        self.tab.addTab(self.tab3, '窗口三')
        self.tab_ui1()
 
    def tab_ui1(self):
        layout = QFormLayout()
        layout.addRow('账号：', QLineEdit())
        layout.addRow('密码：', QLineEdit())
        layout.addRow(QPushButton('点击登陆'))
        self.tab1.setLayout(layout)  # 把布局设置到界面1上面
        self.tab.setTabText(0, '登陆界面')  # 更改界面名称
        self.tab.setTabText(1, '注册界面')
        self.tab.setTabText(2, '找回密码')

class Window2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级控件-QStackedWidget堆栈窗口控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        # 创建列表
        self.lists = QListWidget()
        self.lists.insertItem(0, '登陆界面')
        self.lists.insertItem(1, '注册界面')
        self.lists.insertItem(2, '找回密码')
 
        # 创建三个窗口
        self.win1 = QWidget()
        self.win2 = QWidget()
        self.win3 = QWidget()
 
        # 创建堆栈窗口
        self.stack = QStackedWidget()
        self.stack.addWidget(self.win1)
        self.stack.addWidget(self.win2)
        self.stack.addWidget(self.win3)
 
        # 创建3个窗口内的控件
        layout = QFormLayout()
        layout.addRow('账号：', QLineEdit())
        layout.addRow('密码：', QLineEdit())
        layout.addRow(QPushButton('点击登陆'))
        self.win1.setLayout(layout)
 
        layout1 = QFormLayout()
        layout1.addRow('账号：', QLineEdit())
        layout1.addRow('密码：', QLineEdit())
        layout1.addRow('验证码：', QLineEdit())
        layout1.addRow(QPushButton('点击注册'))
        self.win2.setLayout(layout1)
 
        btn = QPushButton('按钮')
        layout2 = QFormLayout()
        layout2.addWidget(btn)
        self.win3.setLayout(layout2)
 
        # 布局界面
        box = QHBoxLayout()
        box.addWidget(self.lists)
        box.addWidget(self.stack)
        self.setLayout(box)
 
        # 增加点击切换界面
        self.lists.currentRowChanged.connect(self.display)
 
    def display(self, index):
        self.stack.setCurrentIndex(index)

class Window3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级控件-QDockWidget停靠悬浮窗口控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        items = QDockWidget('停靠悬浮窗口', self)
        lists = QListWidget()
        lists.addItem('item1')
        lists.addItem('item2')
        lists.addItem('item3')
        items.setWidget(lists)
 
        items.setFloating(False)

class Window4(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级控件-QScrollBar滚动条控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        self.label = QLabel('QScrollBar滚动条控件')
        # self.label.adjustSize()
 
        self.scr = QScrollBar()
        self.scr.setMaximum(60)
        self.scr.sliderMoved.connect(self.scrmove)
 
        box = QHBoxLayout()
        box.addWidget(self.label)
        box.addWidget(self.scr)
        self.setGeometry(200, 200, 200, 150)
        self.setLayout(box)
 
    def scrmove(self):
        self.label.setFont(QFont('黑体', self.scr.value(), self.scr.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = Window()
    # window.show()
    # window2 = Window2()
    # window2.show()
    # window3 = Window3()
    # window3.show()
    window4 = Window4()
    window4.show()
    sys.exit(app.exec())

'''
from signal import signal
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QObject, Qt, pyqtSignal
# from PyQt6.QtCore.Qt import *
import sys 

class OOO(QObject):
    classSignal = pyqtSignal(int)
    def __init__(self, p):
        QObject.__init__(self, p)
        # self.propertySingal = pyqtSignal(int)

app = QApplication(sys.argv)

def classSlot(var):
    print('classSlot', var)

def propertySingal(var):
    print('propertySingal', var)

w = QWidget()
o = OOO(w)
o.classSignal[int].connect(classSlot)

o2 = OOO(w)

w.show()
o.classSignal.emit(123)
o2.classSignal.emit(456)

sys.exit(app.exec())
'''


'''
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级控件-QTableView二维表格视图控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        # 1.先创建一个数据源模型
        self.model = QStandardItemModel(5, 3)  # 创建5行3列数据模型
        self.model.setHorizontalHeaderLabels(['序号', '姓名', '成绩'])  # 设置数据模型字段
        # 2.创建一个二维表视图控件对象
        self.table = QTableView()
        # 3.和上面的数据源模型进行关联
        self.table.setModel(self.model)
 
        # 创建数据
        item11 = QStandardItem('01')
        item12 = QStandardItem('张三')
        item13 = QStandardItem('61分')
 
        # 添加数据
        self.model.setItem(0, 0, item11)
        self.model.setItem(0, 1, item12)  # 在第一行第二列添加item11
        self.model.setItem(0, 2, item13)
 
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)  # 添加布局到父控件

class Window2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QListView列表数据显示控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        self.model = QStringListModel()  # 创建一个列表数据模型
        self.list = ['列表数据1', '列表数据2', '列表数据3']
        self.model.setStringList(self.list)  # 把数据和数据模型关联起来
 
        self.listview = QListView()  # 创建一个列表数据
        self.listview.setModel(self.model)  # 关联
 
        layout = QVBoxLayout()
        layout.addWidget(self.listview)
        self.setLayout(layout)
 
        self.listview.clicked.connect(self.cao)
 
    def cao(self, item):
        QMessageBox.information(self, 'QListView', '你选择了：' + self.list[item.row()])

class Window3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级控件-QListWidget列表控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        self.listwidget = QListWidget(self)
        self.listwidget.addItem('条目一')
        self.listwidget.addItem('条目二')
        self.listwidget.addItem('条目三')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window2 = Window2()
    window2.show()
    window3 = Window3()
    window3.show()
    sys.exit(app.exec())
'''

'''
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QLCDNumber
from PyQt6.QtCore import QDateTime, QTime, QDate
import sys 
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("展示控件-QLCDNumber面板显示控件 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        lcd = QLCDNumber(6, self)  # 6为展示数字的位数
        lcd2 = QLCDNumber(6, self)  # 6为展示数字的位数
        lcd3 = QLCDNumber(6, self)  # 6为展示数字的位数
        # lcd.setDigitCount(6)  # 单独设置展示位数
        lcd.move(150, 150)
        lcd.resize(300, 60)
        
        lcd2.move(150, 250)
        lcd2.resize(300, 60)
        
        lcd3.move(150, 350)
        lcd3.resize(300, 60)
 
        # 能展示的字符
        # 0 1 2 3 4 5 6 7 8 9
        # A B C D E F g h H L o s S P r u U Y
        # : ' 空格
        # lcd.display('A B C D E')
        lcd.display(123456)  # 整形超出最大展示数值之后就显示0
        lcd2.display(123456)  # 整形超出最大展示数值之后就显示0
        lcd3.display(123456)  # 整形超出最大展示数值之后就显示0
        # lcd.display(123.456)  # 浮点型只展示前6为，小数点为一位
        # lcd.display('123456')
        # print(lcd.intValue())  # 只能获取整型
        # print(lcd.value())  # 只能获取浮点类型
 
        # 模式设置,获取到的数值会自动转为十进制
        lcd.setMode(QLCDNumber.Mode.Bin)  # 二进制      setBinMode()
        lcd2.setMode(QLCDNumber.Mode.Oct)  # 八进制      setOctMode()
        lcd3.setMode(QLCDNumber.Mode.Dec)  # 十进制      setDecMode()
        # lcd.setMode(QLCDNumber.Hex)  # 十六进制     setHexMode()
 
        # 溢出判断
        # print(lcd.checkOverflow(123456789))  # 返回布尔值
 
        # 分段样式 - 创建三个控件对比就知道了
        lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Outline)  # 生成填充背景色的凸起
        lcd2.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)  # 生成填充前景色的凸起
        lcd3.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)  # 生成填充前景色的平坦部分
 
        # 信号
        # lcd.overflow()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
 
    window.show()
    sys.exit(app.exec())
'''


'''
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QDateTimeEdit
from PyQt6.QtCore import QDateTime, QTime, QDate
import sys
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDateTimeEdit时间和日期步长调节器 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
 
    def func(self):
        """
        QDateTimeEdit(parent: QWidget = None)
        QDateTimeEdit(Union[QDateTime, datetime.datetime], parent: QWidget = None)
        QDateTimeEdit(Union[QDate, datetime.date], parent: QWidget = None)
        QDateTimeEdit(Union[QTime, datetime.time], parent: QWidget = None)
        # 从构造函数可以看出，以下三个类没有继承关系
        QDateTime
        QDate
        QTime
        """
        """
        # 简单的构造方法
        self.qsb = QDateTimeEdit(self)  # 直接构造范围最小日期为：1752.9.14，最大日期为：9999.12.31
        self.qsb.resize(150, 40)
        self.qsb.move(150, 150)
 
        self.btn = QPushButton('按钮', self)
        self.btn.resize(60, 30)
        self.btn.move(150, 200)
        self.btn.pressed.connect(self.test)
        """
        # 传入QDateTime的一种构造方法
        # self.dt_tm = QDateTime(2020,1,15,11,31,55)
        self.dt_tm = QDateTime.currentDateTime()  # 当前时间
        self.dt_tm = self.dt_tm.addYears(2)  # 不会直接显示在控件中，要重新赋值
        self.dt_tm.offsetFromUtc()  # 此时与标准时间差
 
        self.qsb = QDateTimeEdit(self.dt_tm, self)
        self.qsb.resize(150, 40)
        self.qsb.move(150, 150)
 
        # QDate和QTime与上面差不多
        # 计时功能
        time = QTime.currentTime()
        # time.start()
        btn = QPushButton(self)
        btn.clicked.connect(lambda: print(time.elapsed() / 1000))
 
        self.qsb1 = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.qsb2 = QDateTimeEdit(QDate.currentDate(), self)
        self.qsb3 = QDateTimeEdit(QTime.currentTime(), self)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
 
    window.show()
    sys.exit(app.exec())
'''


'''
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QLineEdit, QCompleter
from PyQt6.QtGui import QIcon, QAction
import sys

# 制作一个登陆界面，包含账号密码和登陆按钮
# 拥有密码清空和占位提示字符
# 验证账号和密码的正确性
# 如果账号错误，清空表单内容，焦点回到账号栏
# 如果密码错误，清空密码栏，焦点回到密码栏


# class Check_Msg():
#     NAME_ERROR = 1
#     PSD_ERROR = 2
#     SUCCESS = 3
#     @staticmethod   # 本方法不需要实例化，所以直接设置成静态方法
#     def check_login(name,psd):
#         if name != 'aaa':
#             return Check_Msg.NAME_ERROR
#         if psd != '123':
#             return Check_Msg.PSD_ERROR
#         return Check_Msg.SUCCESS
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLineEdit-登陆验证 - PyQt5中文网")
        self.resize(600, 500)
        self.func_list()
 
    def func_list(self):
        self.func()
        self.msgs()
 
    def func(self):
        self.led_name = QLineEdit(self)
        self.led_name.move(150, 50)
        self.btn1 = QPushButton('账号(aaa)', self)
        self.btn1.move(60, 49)
        self.led_name.setPlaceholderText('请输入账号')
        self.led_psd = QLineEdit(self)
        self.led_psd.move(150, 100)
        self.btn2 = QPushButton('密码(123)', self)
        self.btn2.move(60, 99)
        self.led_psd.setPlaceholderText('请输入密码')
        self.led_psd.setEchoMode(QLineEdit.EchoMode.Password)
        self.led_psd.setClearButtonEnabled(True)  # 有内容的时候才会显示
        self.btn_login = QPushButton(self)
        self.btn_login.setText('点击登陆')
        self.btn_login.move(150, 150)
 
        self.btn_login.clicked.connect(self.msgs)
 
    # def msgs(self):
    #     name = self.led_name.text()
    #     psd = self.led_psd.text()
    #     state = Check_Msg.check_login(name,psd)  # 返回的是登陆状态，后面只要判断状态就可以了
    #     if state == 1:
    #         self.led_name.setText('')
    #         self.led_psd.setText('')
    #         self.led_name.setFocus()
    #         print('账号错误')
    #         return None
    #     if state == 2:
    #         self.led_psd.setText('')
    #         self.led_psd.setFocus()
    #         print('密码错误')
    #         return None
    #     if state == 3:
    #         print('登陆成功')
 
    def msgs(self):
        # 获取账号和密码
        name = self.led_name.text()
        psd = self.led_psd.text()
        # 判断账号密码的正确性
        if name != 'aaa':
            self.led_name.setText('')
            self.led_psd.setText('')
            self.led_name.setFocus()
            print('账号错误')
            return None
        if psd != '123':
            self.led_psd.setText('')
            self.led_psd.setFocus()
            print('密码错误')
            return None
        print('验证通过')
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
 
    window.show()
    sys.exit(app.exec())
'''


'''
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QLineEdit, QCompleter
from PyQt6.QtGui import QIcon, QAction
import sys

app = QApplication(sys.argv)
 
window = QWidget()
window.setWindowTitle('QLineEdit-单行文本编辑器 - PyQt5中文网')
window.resize(600,450)
window.move(300,300)
 
btn = QPushButton(window)
btn.move(50,50)
btn.setText('按钮')
 
# 构造
led = QLineEdit(window)
# ==============文本内容的设置和获取=============== # 代码分割线 - 开始


# led.setText('11111')  # 或覆盖构造时默认的文本,这和QPushButton中的setText不一样
# led.insert('22')  # 如果文本框是空的，就和setText是一样的功能
# btn.pressed.connect(lambda :led.insert('WWW'))
# print(led.text())
# btn.pressed.connect(lambda :print(led.text()))
# print(led.displayText())
# btn.pressed.connect(lambda :print(led.displayText()))
# ==============文本内容的设置和获取=============== # 代码分割线 - 结束
# 案例：两个文本框，通过按钮把上一个文本框的内容复制到下一个
# ==============QLineEdit文本框输出模式=============== # 代码分割线 - 开始
# setEchoMode() 明文Normal=0、密文Password=2、不输出NoEcho=1、编辑时明文，结束后密文PasswordEchoOnEdit=3
# 以上的枚举值都是类属性，所以样用QLineEdit调用出来
led.setEchoMode(QLineEdit.EchoMode.Normal)
# ==============QLineEdit文本框输出模式=============== # 代码分割线 - 结束
 
# ==============QLineEdit占位提示=============== # 代码分割线 - 开始
# setPlaceholderText()
# placeholderText()
led.setPlaceholderText('请输入密码')
# ==============QLineEdit占位提示=============== # 代码分割线 - 结束
 
# ==============QLineEdit清空按钮=============== # 代码分割线 - 开始
led.setClearButtonEnabled(True)
# ==============QLineEdit清空按钮=============== # 代码分割线 - 结束
 
# ==============QLineEdit添加明文/密文操作行为=============== # 代码分割线 - 开始
action = QAction(led)  # 创建一个QAction对象放在led表单中
action.setIcon(QIcon('close.png'))  # 给对象设置图标
def change():
    if led.echoMode() == QLineEdit.EchoMode.Normal:
        led.setEchoMode(QLineEdit.EchoMode.Password)
        action.setIcon(QIcon('close.png'))
    else:
        led.setEchoMode(QLineEdit.EchoMode.Normal)
        action.setIcon(QIcon('open.png'))
action.triggered.connect(change)
led.addAction(action,QLineEdit.ActionPosition.TrailingPosition) # 接收对象，指定存放位置
# ==============QLineEdit添加明文/密文操作行为=============== # 代码分割线 - 结束
 
# ==============QLineEdit自动补全=============== # 代码分割线 - 开始
qcompleter = QCompleter(['aaa','abc','AAA','123','136'],led)
led.setCompleter(qcompleter)  # led改为明文显示
# ==============QLineEdit自动补全=============== # 代码分割线 - 结束
 
# ==============输入限制=============== # 代码分割线 - 开始
led.setMaxLength(5)   # 字符长度限制
led.setReadOnly(True)   # 制度设置
# ==============输入限制=============== # 代码分割线 - 结束
 
window.show()
sys.exit(app.exec())
'''


'''
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
import sys

class Window(QWidget):
    # QContextMenuEvent
    def contextMenuEvent(self, evt):
        menu = QMenu(self)
        menuAction1 = QAction(QIcon('123.jpg'), '菜单1', self)
        menuAction1.triggered.connect(lambda: print('WWWWWW'))
        menu.addAction(menuAction1)
        menu.exec_(evt.globalPos())
 
 
app = QApplication(sys.argv)
 
window = Window()
window.setWindowTitle('QPushButton - PyQt5中文网')
window.resize(600,450)
window.move(300,300)
 
btn4 = QPushButton(QIcon('123.jpg'),'按钮',window)
# ==============控件菜单设置=============== # 代码分割线 - 开始
# 上面需要创建一个按钮
# 创建菜单对象
menu = QMenu()  # 菜单中不要创建文本和图标，会被上面的主按钮覆盖
# 构造一个菜单选项
menuAction1 = QAction(QIcon('123.jpg'),'菜单1',window)
menuAction1.triggered.connect(lambda : print('WWWWWW'))
# 添加菜单列表
menu.addAction(menuAction1)
btn4.setMenu(menu)
# ==============控件菜单设置=============== # 代码分割线 - 结束
 
# ==============按钮扁平化处理=============== # 代码分割线 - 开始
# btn4.setStyleSheet('background-color:green')
# btn4.setFlat(True)
# ==============按钮扁平化处理=============== # 代码分割线 - 结束
 
# ==============默认按钮处理=============== # 代码分割线 - 开始
btn5 = QPushButton(window)
btn5.setText('默认按钮')
btn5.move(150,150)
btn6 = QPushButton(window)
btn6.setText('默认按钮')
btn6.move(150,200)
btn6.setAutoDefault(True)  # 点击后会焦点停留
btn6.setDefault(True)  # 点击前自动默认
# ==============默认按钮处理=============== # 代码分割线 - 结束
 
# ==============右键菜单=============== # 代码分割线 - 开始
# 第一种方法：上面创建的类中
# 第二种方法：下面的right_menu函数中
def right_menu(point):
    menu = QMenu(window)
    menuAction1 = QAction(QIcon('123.jpg'), '菜单1', window)
    menuAction1.triggered.connect(lambda: print('QQQQ'))
    menu.addAction(menuAction1)
    menu.exec(window.mapToGlobal(point))
 
# window.setContextMenuPolicy(Qt.DefaultContextMenu)
window.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
window.customContextMenuRequested.connect(right_menu)
# ==============右键菜单=============== # 代码分割线 - 结束
 
window.show()
sys.exit(app.exec())
'''

'''
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QMenu
from PyQt6.QtGui import QIcon, QAction
import sys

# setMenu(QMenu)   设置菜单
# menu()    获取菜单
# showMenu()   展示菜单
# QMenu()继承自QWidget
# addMenu(QMenu)   添加子菜单
# addSeparator()   添加分割线
# addAction(QAction)  添加行为动作
# QMenu控件设置：setTitle()  setIcon(QIcon)
# QAction设置：setText()  setIcon(QIcon)  信号：triggered

app = QApplication(sys.argv)
 
window = QWidget()
window.setWindowTitle('QPushButton - PyQt5中文网')
window.resize(600,450)
window.move(300,300)
 
# ==============QPushbutton的构造函数=============== # 代码分割线 - 开始
# btn1 = QPushButton()
# btn2 = QPushButton(window)
# btn3 = QPushButton('按钮',window)
btn4 = QPushButton(QIcon('123.jpg'),'按钮',window)
# ==============QPushbutton的构造函数=============== # 代码分割线 - 结束
 
# ==============控件菜单设置=============== # 代码分割线 - 开始
# 流程参考test.py
# 创建菜单对象
menu = QMenu()
sun_menu = QMenu(menu)  # 放在父菜单中
sun_menu.setTitle('子菜单标题')
# 构造一个菜单
menuAction1 = QAction(QIcon('123.jpg'),'菜单1',window)
menuAction1.triggered.connect(lambda : print('WWWWWW'))
 
menuAction2 = QAction(QIcon('123.jpg'),'菜单2',window)
menuAction2.triggered.connect(lambda : print('SSSSSSSS'))
 
menuAction3 = QAction('菜单3',window)
menuAction3.triggered.connect(lambda : print('AAAAA'))
# 构造一个子菜单
sun_menuAction = QAction(QIcon('123.jpg'),'子菜单1',window)
# 添加菜单列表
menu.addAction(menuAction1)
menu.addAction(menuAction2)
menu.addSeparator()  # 添加分割线
menu.addMenu(sun_menu)  # 先在主菜单栏中添加一个子菜单
sun_menu.addAction(sun_menuAction)  # 然后为上面的子菜单添加子菜单
menu.addAction(menuAction3)
 
btn4.setMenu(menu)
# btn4.showMenu()  # 继承与QWidget所以可以单独展示
# ==============控件菜单设置=============== # 代码分割线 - 结束
 
# window.show()
btn4.showMenu()
sys.exit(app.exec())
'''

'''
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication
import sys

app = QApplication(sys.argv)
 
window = QWidget()
window.setWindowTitle('QAbstractButton - PyQt5中文网')
window.resize(600, 450)
window.move(300, 300)
 
 
class Btn2(QPushButton):
    def hitButton(self, poi):
        # return False
        print(poi)
        if poi.x() > self.width() / 2:
            return True
        return False
 
 
btn6 = Btn2(window)
btn6.setText('有效区域')
btn6.move(0, 300)
btn6.setChecked(True)
btn6.pressed.connect(lambda: print('pressed ========='))
btn6.released.connect(lambda: print('released ========='))
btn6.clicked.connect(lambda val: print('clicked =========', val))
btn6.toggled.connect(lambda val: print('toggled =========', val))
 
window.show()
sys.exit(app.exec())
'''