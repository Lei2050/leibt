from tabnanny import check
from PyQt6.QtCore import QCoreApplication, QObject
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView

import view.gg as view_gg
import data.control as control
import view.standard_item as standard_item
from g.config import Config
import view.actions as actions

import data.item as data_item

class MainWindowFixer(QObject):
    def __init__(self, ui):
        self.ui = ui

    def setup(self):
        self.setupMenusBar()
        self.setupWorkspaceTreeView()
        self.setupControlTreeView()
        self.setupPropertyStackedWidget()
    
    def _clearAllEnvAction(self):
        actionMenus = [self.ui.actionDebug, self.ui.actionRelease]
        for v in actionMenus:
            v.setChecked(False)
    def _onShiftEnv(self, checked, a):
        self._clearAllEnvAction()
        a.setChecked(True)
        actionMenus = {self.ui.actionDebug: 'debug', self.ui.actionRelease: 'release'}
        Config().saveEnv(actionMenus.get(a, ''))
    
    def setupMenusBar(self):
        # self.ui.action_new_workspace.triggered.connect(self.actionNewWorkspace) #为什么这样触发不了？？？
        self.ui.action_new_workspace.triggered.connect(actions.ActionNewWorkspace)
        self.ui.action_open_workspace.triggered.connect(actions.ActionOpenWorkspace)
        self.ui.action_scene_setting.triggered.connect(actions.ActionSceneSetting)
        self.ui.actionDebug.triggered.connect(lambda checked, a=self.ui.actionDebug: self._onShiftEnv(checked, a))
        self.ui.actionRelease.triggered.connect(lambda checked, a=self.ui.actionRelease: self._onShiftEnv(checked, a))
        env = Config().loadEnv()
        if env == 'debug':
            self.ui.actionDebug.setChecked(True)
        else:
            self.ui.actionRelease.setChecked(True)
        '''
        self.menu_file.addAction(self.action_new_workspace)
        self.menu_file.addAction(self.action_open_workspace)
        self.menu_file.addAction(self.action_edit_workspace)
        self.menu_file.addAction(self.action_reload_workspace)
        '''

    def _setupTreeViewNode(self, parent, nodeInfo):
        _translate = QCoreApplication.translate
        itemData = data_item.Data.get(nodeInfo['type'], None)
        iconName = 'directory.png' if nodeInfo.get('subs') else itemData.get('icon')
        item = standard_item.StandardItemControl(_translate("MainWindow", nodeInfo['name']), iconName, nodeInfo['type'])
        parent.appendRow(item)
        for node in nodeInfo.get('subs', []):
            self._setupTreeViewNode(item, node)

    def setupWorkspaceTreeView(self):
        treeView = self.ui.treeViewWorkspace
        # treeModel = QStandardItemModel()
        # rootNode = treeModel.invisibleRootItem()
        self.ui.widgetWorkspaceNewToolButton.clicked.connect(actions.ActionNewWorkspace)
        self.ui.widgetWorkspaceOpenToolButton.clicked.connect(actions.ActionOpenWorkspace)
        self.ui.widgetWorkspaceExpandAllToolButton.clicked.connect(lambda: treeView.expandAll())
        self.ui.widgetWorkspaceCollapseAllToolButton.clicked.connect(lambda: treeView.collapseAll())

    def setupControlTreeView(self):
        treeView = self.ui.treeViewNodes
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for nodeInfo in control.Data:
            self._setupTreeViewNode(rootNode, nodeInfo)
        
        treeView.setModel(treeModel)
        treeView.expandAll()
        treeView.setHeaderHidden(True)

        treeView.setDragEnabled(True)
        # treeView.setDropIndicatorShown(True)
        treeView.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)

        self.ui.widgetNodesExpandAllToolButton.clicked.connect(lambda: treeView.expandAll())
        self.ui.widgetNodesCollapseAllToolButton.clicked.connect(lambda: treeView.collapseAll())
    
    def setupPropertyStackedWidget(self):
        view_gg.PropertyStackedWidget = self.ui.stackedWidget
        view_gg.PropertyStackedWidget.setup()
        view_gg.CommentPlainTextEdit = self.ui.plainTextEditComment
        view_gg.InfoPlainTextEdit = self.ui.plainTextEdit
        view_gg.WorkspaceTreeView = self.ui.treeViewWorkspace
        view_gg.SceneTabWidget = self.ui.tabWidgetBTView
        