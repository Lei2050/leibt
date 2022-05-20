# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QMessageBox

import view.tree_view_nodes as tree_view_nodes
import view.tree_view_workspace as tree_view_workspace
import view.tab_widget_scene as tab_widget_scene
import view.stacked_widget_property as stacked_widget_property
from view.main_window_fix import MainWindowFixer
import view.gg as view_gg
import view.actions as actions
from g.config import Config

class MainWindow(QtWidgets.QMainWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    #打开某棵行为树，list为路径
    OpenTree = QtCore.pyqtSignal(list)
    #tabWidget当前场景发生改变
    ViewSceneChanged = QtCore.pyqtSignal(list)
    #删除工作区
    WorkspaceDeleted = QtCore.pyqtSignal(str)
    #删除目录
    DirectoryDeleted = QtCore.pyqtSignal(list)
    #删除行为树
    TreeDeleted = QtCore.pyqtSignal(list)
    #工作区打开了
    WorkspaceOpened = QtCore.pyqtSignal(str)
    #工作区重命名
    WorkspaceRenamed = QtCore.pyqtSignal(str, str)
    #目录重命名
    DirRenamed = QtCore.pyqtSignal(list, str)
    #行为树重命名
    TreeRenamed = QtCore.pyqtSignal(list, str)
    #窗口都准备好了
    MainWindowSetuped = QtCore.pyqtSignal()
    #场景配置变更
    SceneSettingChanged = QtCore.pyqtSignal()
    #行为树有变更，要提示当前文件未保存
    #list - path
    #bool - 是否已保存
    TreeChanged = QtCore.pyqtSignal(list, bool)
    #整个工作区保存成功
    WorkspaceSaved = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        view_gg.MainWindow = self

        ui = Ui_MainWindow()
        ui.setupUi(self)
        
        mwf = MainWindowFixer(ui)
        mwf.setup()
        
        self.keyPressed.connect(ui.tabWidgetBTView.onKeyPress)
        self.WorkspaceOpened.connect(actions.ActionWorkspaceOpened)
        self.MainWindowSetuped.connect(actions.ActionAfterMainWindowSetuped)

        #恢复上一次窗口位置和大小
        geo = Config().loadMainwindowGeometry()
        if geo:
            self.setGeometry(QRect(geo[0], geo[1], geo[2], geo[3]))
        #这里最后执行
        self.MainWindowSetuped.emit()

    def keyPressEvent(self, event):
        super(MainWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event)
    
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        #保存当前窗口位置和大小
        g = self.geometry()
        Config().saveMainwindowGeometry([g.x(), g.y(), g.width(), g.height()])
    
    def closeEvent(self, event):
        unsavedWorkspaces = view_gg.WorkspaceTreeView.getUnsavedWorkspaces()
        if len(unsavedWorkspaces) <= 0:
            event.accept()
            return
        
        msg = '以下工作区含有未保存文件：\n' + '\n'.join(unsavedWorkspaces) + '\n确定仍要关闭软件吗？'
        reply = QMessageBox.question(self, '警告', msg,
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1360, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.splitter_3 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_3.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter = QtWidgets.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.widgetWorkspace = QtWidgets.QWidget(self.splitter)
        self.widgetWorkspace.setObjectName("widgetWorkspace")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widgetWorkspace)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.wsHLayout = QtWidgets.QHBoxLayout()
        self.wsHLayout.setObjectName("wsHLayout")
        self.widgetWorkspaceNewToolButton = QtWidgets.QToolButton(self.widgetWorkspace)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/icon/new_workspace.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.widgetWorkspaceNewToolButton.setIcon(icon)
        self.widgetWorkspaceNewToolButton.setIconSize(QtCore.QSize(16, 16))
        self.widgetWorkspaceNewToolButton.setObjectName("widgetWorkspaceNewToolButton")
        self.widgetWorkspaceNewToolButton.setToolTip('新建工作区')
        self.wsHLayout.addWidget(self.widgetWorkspaceNewToolButton)
        self.widgetWorkspaceOpenToolButton = QtWidgets.QToolButton(self.widgetWorkspace)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/icon/open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.widgetWorkspaceOpenToolButton.setIcon(icon)
        self.widgetWorkspaceOpenToolButton.setIconSize(QtCore.QSize(16, 16))
        self.widgetWorkspaceOpenToolButton.setObjectName("widgetWorkspaceOpenToolButton")
        self.widgetWorkspaceOpenToolButton.setToolTip('打开工作区')
        self.wsHLayout.addWidget(self.widgetWorkspaceOpenToolButton)
        self.line_1 = QtWidgets.QFrame(self.widgetWorkspace)
        self.line_1.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_1.setObjectName("line_1")
        self.wsHLayout.addWidget(self.line_1)
        self.widgetWorkspaceExpandAllToolButton = QtWidgets.QToolButton(self.widgetWorkspace)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/icon/plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.widgetWorkspaceExpandAllToolButton.setIcon(icon)
        self.widgetWorkspaceExpandAllToolButton.setIconSize(QtCore.QSize(16, 16))
        self.widgetWorkspaceExpandAllToolButton.setObjectName("widgetWorkspaceExpandAllToolButton")
        self.widgetWorkspaceExpandAllToolButton.setToolTip('展开全部')
        self.wsHLayout.addWidget(self.widgetWorkspaceExpandAllToolButton)
        self.widgetWorkspaceCollapseAllToolButton = QtWidgets.QToolButton(self.widgetWorkspace)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resource/icon/minus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.widgetWorkspaceCollapseAllToolButton.setIcon(icon1)
        self.widgetWorkspaceCollapseAllToolButton.setObjectName("widgetWorkspaceCollapseAllToolButton")
        self.widgetWorkspaceCollapseAllToolButton.setToolTip('收起全部')
        self.wsHLayout.addWidget(self.widgetWorkspaceCollapseAllToolButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.wsHLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.wsHLayout)
        # self.treeViewWorkspace = QtWidgets.QTreeView(self.widgetWorkspace)
        self.treeViewWorkspace = tree_view_workspace.TreeViewWorkspace(self.widgetWorkspace)
        self.treeViewWorkspace.setObjectName("treeViewWorkspace")
        self.verticalLayout_2.addWidget(self.treeViewWorkspace)
        self.widgetNodes = QtWidgets.QWidget(self.splitter)
        self.widgetNodes.setObjectName("widgetNodes")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widgetNodes)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widgetNodesExpandAllToolButton = QtWidgets.QToolButton(self.widgetNodes)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resource/icon/plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.widgetNodesExpandAllToolButton.setIcon(icon2)
        self.widgetNodesExpandAllToolButton.setIconSize(QtCore.QSize(16, 16))
        self.widgetNodesExpandAllToolButton.setObjectName("widgetNodesExpandAllToolButton")
        self.widgetNodesExpandAllToolButton.setToolTip('展开全部')
        self.horizontalLayout_3.addWidget(self.widgetNodesExpandAllToolButton)
        self.widgetNodesCollapseAllToolButton = QtWidgets.QToolButton(self.widgetNodes)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resource/icon/minus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.widgetNodesCollapseAllToolButton.setIcon(icon1)
        self.widgetNodesCollapseAllToolButton.setObjectName("widgetNodesCollapseAllToolButton")
        self.widgetNodesCollapseAllToolButton.setToolTip('收起全部')
        self.horizontalLayout_3.addWidget(self.widgetNodesCollapseAllToolButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        # self.treeViewNodes = QtWidgets.QTreeView(self.widgetNodes)
        self.treeViewNodes = tree_view_nodes.TreeViewNodes(self.widgetNodes)
        self.treeViewNodes.setObjectName("treeViewNodes")
        self.verticalLayout_3.addWidget(self.treeViewNodes)
        # self.tabWidgetBTView = QtWidgets.QTabWidget(self.splitter_3)
        self.tabWidgetBTView = tab_widget_scene.TabWidgetScene(self.splitter_3)
        self.tabWidgetBTView.setMovable(True)
        self.tabWidgetBTView.setObjectName("tabWidgetBTView")
        # self.tab = QtWidgets.QWidget()
        # self.tab.setObjectName("tab")
        # self.tabWidgetBTView.addTab(self.tab, "")
        # self.tab_2 = QtWidgets.QWidget()
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidgetBTView.addTab(self.tab_2, "")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        # self.stackedWidget = QtWidgets.QStackedWidget(self.splitter_2)
        # self.stackedWidget.setObjectName("stackedWidget")
        # self.page = QtWidgets.QWidget()
        # self.page.setObjectName("page")
        # self.stackedWidget.addWidget(self.page)
        # self.page_2 = QtWidgets.QWidget()
        # self.page_2.setObjectName("page_2")
        # self.stackedWidget.addWidget(self.page_2)

        self.stackedWidget = stacked_widget_property.StackedWidgetProperty(self.splitter_2)
        # self.stackedWidget = QtWidgets.QStackedWidget(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMouseTracking(False)
        self.stackedWidget.setObjectName("stackedWidget")
        # self.stackedWidget.setup()
        
        self.widget = QtWidgets.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(8, 0, 8, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEditComment = QtWidgets.QPlainTextEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEditComment.sizePolicy().hasHeightForWidth())
        self.plainTextEditComment.setSizePolicy(sizePolicy)
        self.plainTextEditComment.setReadOnly(True)
        self.plainTextEditComment.setObjectName("plainTextEditComment")
        self.gridLayout.addWidget(self.plainTextEditComment, 0, 0, 1, 1)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.splitter_4)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_3.addWidget(self.splitter_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1227, 23))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_edit = QtWidgets.QMenu(self.menubar)
        self.menu_edit.setObjectName("menu_edit")
        self.menu_view = QtWidgets.QMenu(self.menubar)
        self.menu_view.setObjectName("menu_view")
        self.menu_debug = QtWidgets.QMenu(self.menubar)
        self.menu_debug.setObjectName("menu_debug")
        self.menu_shift_env = QtWidgets.QMenu(self.menu_debug)
        self.menu_shift_env.setObjectName("menu_shift_env")
        self.menu_setting = QtWidgets.QMenu(self.menubar)
        self.menu_setting.setObjectName("menu_setting")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.action_new_workspace = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/icon/new_workspace.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_new_workspace.setIcon(icon)
        self.action_new_workspace.setObjectName("action_new_workspace")
        self.action_open_workspace = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/icon/open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_open_workspace.setIcon(icon)
        self.action_open_workspace.setObjectName("action_open_workspace")
        # self.action_edit_workspace = QtGui.QAction(MainWindow)
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("resource/icon/open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        # self.action_edit_workspace.setIcon(icon)
        # self.action_edit_workspace.setObjectName("action_edit_workspace")
        # self.action_reload_workspace = QtGui.QAction(MainWindow)
        # self.action_reload_workspace.setObjectName("action_reload_workspace")
        # self.action_new_tree = QtGui.QAction(MainWindow)
        # icon3 = QtGui.QIcon()
        # icon3.addPixmap(QtGui.QPixmap("resource/icon/new_tree.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        # self.action_new_tree.setIcon(icon3)
        # self.action_new_tree.setObjectName("action_new_tree")
        self.actionDebug = QtGui.QAction(MainWindow)
        self.actionDebug.setCheckable(True)
        self.actionDebug.setObjectName("actionDebug")
        self.actionRelease = QtGui.QAction(MainWindow)
        self.actionRelease.setCheckable(True)
        self.actionRelease.setObjectName("actionRelease")
        self.menu_file.addAction(self.action_new_workspace)
        self.menu_file.addAction(self.action_open_workspace)
        # self.menu_file.addAction(self.action_edit_workspace)
        # self.menu_file.addAction(self.action_reload_workspace)
        self.menu_file.addSeparator()
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menu_shift_env.addAction(self.actionDebug)
        self.menu_shift_env.addAction(self.actionRelease)
        self.menu_debug.addAction(self.menu_shift_env.menuAction())
        self.menubar.addAction(self.menu_debug.menuAction())
        self.action_scene_setting = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/icon/setting.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_scene_setting.setIcon(icon)
        self.action_scene_setting.setObjectName("action_scene_setting")
        self.menu_setting.addAction(self.action_scene_setting)
        self.menubar.addAction(self.menu_setting.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.toolBar.addAction(self.action_new_workspace)
        self.toolBar.addAction(self.action_open_workspace)

        self.retranslateUi(MainWindow)
        # self.tabWidgetBTView.setCurrentIndex(0)
        # self.stackedWidget.setCurrentIndex(1) #在fix中显示
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        sizes = []
        sizes.append(int(0.2 * MainWindow.sizeHint().width()))
        sizes.append(int(0.6 * MainWindow.sizeHint().width()))
        sizes.append(int(0.2 * MainWindow.sizeHint().width()))
        self.splitter_3.setSizes(sizes)

        winHeight = MainWindow.sizeHint().height()
        sizes = []
        sizes.append(int(0.8 * winHeight))
        sizes.append(int(0.2 * winHeight))
        self.splitter_4.setSizes(sizes)

        winHeight = 0.9 * winHeight
        sizes = []
        sizes.append(int(0.3 * winHeight))
        sizes.append(int(0.7 * winHeight))
        self.splitter.setSizes(sizes)

        sizes = []
        sizes.append(int(0.8 * winHeight))
        sizes.append(int(0.2 * winHeight))
        self.splitter_2.setSizes(sizes)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.widgetWorkspaceOpenToolButton.setText(_translate("MainWindow", "..."))
        self.widgetWorkspaceExpandAllToolButton.setText(_translate("MainWindow", "..."))
        self.widgetWorkspaceCollapseAllToolButton.setText(_translate("MainWindow", "..."))
        self.widgetNodesExpandAllToolButton.setText(_translate("MainWindow", "..."))
        self.widgetNodesCollapseAllToolButton.setText(_translate("MainWindow", "..."))
        # self.tabWidgetBTView.setTabText(self.tabWidgetBTView.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        # self.tabWidgetBTView.setTabText(self.tabWidgetBTView.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        # self.plainTextEdit.setPlainText(_translate("MainWindow", "行为树有错误"))
        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.menu_edit.setTitle(_translate("MainWindow", "编辑"))
        self.menu_view.setTitle(_translate("MainWindow", "视图"))
        self.menu_debug.setTitle(_translate("MainWindow", "调试"))
        self.menu_shift_env.setTitle(_translate("MainWindow", "切换该软件模式"))
        self.menu_setting.setTitle(_translate("MainWindow", "设置"))
        self.menu_help.setTitle(_translate("MainWindow", "帮助"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_new_workspace.setText(_translate("MainWindow", "新建工作区"))
        self.action_open_workspace.setText(_translate("MainWindow", "打开工作区"))
        self.action_open_workspace.setIconText(_translate("MainWindow", "打开工作区"))
        self.action_open_workspace.setShortcut(_translate("MainWindow", "Ctrl+W"))
        # self.action_edit_workspace.setText(_translate("MainWindow", "编辑工作区"))
        # self.action_reload_workspace.setText(_translate("MainWindow", "重新加载工作区"))
        # self.action_reload_workspace.setShortcut(_translate("MainWindow", "Ctrl+R"))
        # self.action_new_tree.setText(_translate("MainWindow", "新建行为树"))
        # self.action_new_tree.setToolTip(_translate("MainWindow", "<html><head/><body><p>新建行为树</p></body></html>"))
        # self.action_new_tree.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_scene_setting.setText(_translate("MainWindow", "场景"))
        self.actionDebug.setText(_translate("MainWindow", "Debug"))
        self.actionRelease.setText(_translate("MainWindow", "Release"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())