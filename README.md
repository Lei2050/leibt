# leibt
behavior tree for kbengine

行为树可视化编辑工具，可以导出python代码，方便在kbengine中使用。

## 依赖：
- python（建议3.9版本）
- pyqt6

## 使用：
1，运行：工程跟目录下执行：py main.py  
也可以使用pyinstaller打包成exe。

2，新建或打开工作区，在工作区中右击创建行为树，从左侧控件中拖动控件进行编辑。。。

3，右击工作区，导出工作区。

4，将导出的代码目录"btpy"复制到kbengine服务器目录assets/scripts下；同时把leibt工程根目录下的btpy目录也复制到服务器目录assets/scripts下（合并）。

![leibt_btpy](https://user-images.githubusercontent.com/8241429/169568824-23c9a7e9-df27-4917-b168-d7d755f097dd.jpg)

5，在需要使用行为树的Entity中：

import btpy.btpy_hello as btpy_hello

self.bt = btpy_hello.Create(self)

6，在定时器中执行行为树tick：

self.bt.exec()

## 主界面展示：
![leibt](https://user-images.githubusercontent.com/8241429/169566855-c0745231-8181-4b80-9fa8-3fb703524609.jpg)
