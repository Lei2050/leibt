from tkinter.filedialog import SaveAs
from PyQt6.QtWidgets import QTreeView, QAbstractItemView, QMenu, QInputDialog
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap, QAction, QCursor, QFont, QColor

from controller.controller import Controller
from g.config import Config
import view.actions as actions
import g.gg as gg
import view.gg as view_gg
import common.utils as utils
from view.dialog_scene_setting import DialogSceneSetting

class TreeViewWorkspaceStandardItem(QStandardItem):
    TypeWorkspace = 1
    TypeDirectory = 2
    TypeTree = 3

    def __init__(self, parent, name='', typ = 0, font_size=12, set_bold=False):
        super(QStandardItem, self).__init__(parent)

        self.name = name
        self.typ = typ

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        # self.setForeground(QColor(255, 0, 0))
        # self.setBackground(QColor(255, 0, 0))
        self.setFont(fnt)
        self.setText(self.name)

        icon = 'tree.png'
        if self.typ == self.TypeWorkspace:
            icon = 'workspace.png'
        elif self.typ == self.TypeDirectory:
            icon = 'directory.png'
        ic = QIcon()
        ic.addPixmap(QPixmap(gg.IconPrefix + icon), QIcon.Mode.Normal, QIcon.State.Off)
        self.setIcon(ic)
    
    def getWorkspaceName(self):
        sitem = self
        pitem = sitem.parent()
        while pitem:
            sitem = pitem
            pitem = sitem.parent()
        return sitem.name
    
    def getPath(self):
        path = []
        sitem = self
        while sitem:
            path.append(sitem.name)
            sitem = sitem.parent()
        path.reverse()
        return path
    
    #找到该节点下的所有子节点，不仅仅是第一级子节点
    #返回的节点包括自己（第一个）
    def getAllChildren(self, filter = None) -> list:
        ret = []
        if not filter or filter(self):
            ret.append(self)
        rowCount = self.rowCount()
        for i in range(rowCount):
            child = self.child(i)
            ret = ret + child.getAllChildren(filter)
        return ret
    
    #对一级子节点进行统计，filter-统计条件
    def countFirstLevelChildren(self, filter = None) -> int:
        c = 0
        rowCount = self.rowCount()
        for i in range(rowCount):
            child = self.child(i)
            if not filter or filter(child):
                c += 1
        return c
    
    def setSavedFlag(self, saved: bool):
        self.setText(self.name + ('' if saved else " *"))
    
    def isSaved(self) -> bool:
        return not self.text().endswith('*')
    
    def setName(self, name):
        self.name = name
        self.setSavedFlag(self.isSaved())

class TreeViewWorkspace(QTreeView):
    NewWorkspace = pyqtSignal(str)
    WorkspaceSaved = pyqtSignal(str)
    AddNewTree = pyqtSignal(list)

    def __init__(self, parent):
        super(QTreeView, self).__init__(parent)

        self.treeModel = QStandardItemModel()
        self.rootNode = self.treeModel.invisibleRootItem()
        self.setModel(self.treeModel)
        self.setHeaderHidden(True)
        self.setDragEnabled(False)
        self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.customContextMenuRequested.connect(self._showContextMenu)
        self.NewWorkspace.connect(self.addWorkspace)
        self.AddNewTree.connect(self.onAddNewTree)
        self.doubleClicked.connect(self.onDoubleClicked)
        # view_gg.MainWindow.OpenTree.connect(self.onTreeOpen)
        view_gg.MainWindow.ViewSceneChanged.connect(self.onOpenedTreeChanged)
        view_gg.MainWindow.WorkspaceDeleted.connect(self.onWorkspaceDeleted)
        view_gg.MainWindow.DirectoryDeleted.connect(self.onDirectoryDeleted)
        view_gg.MainWindow.TreeDeleted.connect(self.onTreeDeleted)
        view_gg.MainWindow.SceneSettingChanged.connect(self.onSceneSettingChanged)
        view_gg.MainWindow.TreeChanged.connect(self.onTreeChanged)
        view_gg.MainWindow.WorkspaceSaved.connect(self.onWorkspaceSaved)
        view_gg.MainWindow.WorkspaceRenamed.connect(self.onWorkspaceRenamed)
        view_gg.MainWindow.DirRenamed.connect(self.onDirRenamed)
        view_gg.MainWindow.TreeRenamed.connect(self.onTreeRenamed)

        # self.workspaceNames = set({})
        self.currentOpenItem = None #当前在场景打开的行为树
    
    def addWorkspace(self, name):
        _translate = QCoreApplication.translate

        item = TreeViewWorkspaceStandardItem(None, _translate("MainWindow", name), TreeViewWorkspaceStandardItem.TypeWorkspace)

        self.rootNode.insertRow(0, [item])
        self.treeModel.sort(0)
    
    def _findChildByName(self, item, name, itemTypes = []):
        rowCount = item.rowCount()
        #因为是有序，所以用二分查找
        l, h = 0, rowCount - 1
        m = 0
        while l <= h:
            m = (l + h) >> 1
            text = item.child(m).name
            if text == name:
                break
            elif text < name:
                l = m + 1
            else:
                h = m - 1
        if l > h:
            return None
        #子节点中可能有两个相同text的节点，但是typ不一样
        for i in range(m, rowCount):
            child = item.child(i)
            if child.name == name and (not itemTypes or child.typ in itemTypes):
                return child
        for i in range(m - 1, -1, -1):
            child = item.child(i)
            if child.name == name and (not itemTypes or child.typ in itemTypes):
                return child
        return None
    
    def findItemByPath(self, path, itemTypes = []):
        if not path:
            return None
        item = self.rootNode
        for name in path[:-1]:
            #路径中间的肯定都是工作空间or目录
            item = self._findChildByName(item, name, [TreeViewWorkspaceStandardItem.TypeWorkspace, TreeViewWorkspaceStandardItem.TypeDirectory])
            if not item:
                return None
        return self._findChildByName(item, path[-1], itemTypes)
    
    #找到item的所有父节点，倒序
    def findParentsByItem(self, item) -> list:
        ret = []
        parent = item.parent()
        while parent:
            ret.append(parent)
            parent = parent.parent()
        return ret
    
    def findWorkspaceItemByName(self, name):
        for i in range(self.rootNode.rowCount()):
            child = self.rootNode.child(i)
            if child.name == name:
                return child
        return None
    
    def onWorkspaceRenamed(self, oldName, newName):
        Config().remWorkspace(oldName)
        item = self.findWorkspaceItemByName(oldName)
        if not item:
            return
        item.setName(newName)
        self.treeModel.sort(0)
        actions.ActionAddWorkspaceIntoCONFIG(newName)
    
    def onDirRenamed(self, path, newName):
        item = self.findItemByPath(path)
        if not item:
            return
        item.setName(newName)
        self.treeModel.sort(0)
    
    def onTreeRenamed(self, path, newName):
        item = self.findItemByPath(path)
        if not item:
            return
        item.setName(newName)
        self.treeModel.sort(0)
    
    def onAddNewTree(self, path):
        item = self.findItemByPath(path[:-1], [TreeViewWorkspaceStandardItem.TypeWorkspace, TreeViewWorkspaceStandardItem.TypeDirectory])
        subItem = TreeViewWorkspaceStandardItem(item, path[-1], TreeViewWorkspaceStandardItem.TypeTree)
        item.insertRow(0, [subItem])
        self.treeModel.sort(0)
        self.expand(item.index())
    
    #点击空白地方时的菜单
    def _simpleContextMenu(self):
        popMenu = QMenu()
        newWorkspaceAction = QAction(u'新建工作区', self)
        newWorkspaceAction.triggered.connect(actions.ActionNewWorkspace)
        popMenu.addAction(newWorkspaceAction)
        openWorkspaceAction = QAction(u'打开工作区', self)
        openWorkspaceAction.triggered.connect(actions.ActionOpenWorkspace)
        popMenu.addAction(openWorkspaceAction)
        return popMenu
    
    #右击工作空间时的菜单
    def _onWorkspaceContextMenu(self, modelIndex):
        item = self.treeModel.itemFromIndex(modelIndex)
        workspaceName = item.getWorkspaceName()

        popMenu = QMenu()
        expandAction = QAction(u'展开', self)
        expandAction.triggered.connect(lambda: self._actionExpand(modelIndex))
        popMenu.addAction(expandAction)
        collapseAction = QAction(u'收起', self)
        collapseAction.triggered.connect(lambda: self._actionCollapse(modelIndex))
        popMenu.addAction(collapseAction)
        popMenu.addSeparator()

        newDirAction = QAction(u'新建目录', self)
        newDirAction.triggered.connect(lambda: self._actionNewDirectory(item))
        popMenu.addAction(newDirAction)
        newTreection = QAction(u'新建行为树', self)
        newTreection.triggered.connect(lambda: self._actionNewTree(item))
        popMenu.addAction(newTreection)
        importTeeAction = QAction(u'导入行为树', self)
        importTeeAction.triggered.connect(lambda: self._actionImportTree(item))
        popMenu.addAction(importTeeAction)
        editWorkspaceAction = QAction(u'编辑工作区', self)
        editWorkspaceAction.triggered.connect(lambda: actions.ActionEditWorkspace(workspaceName))
        popMenu.addAction(editWorkspaceAction)
        reloadWorkspaceAction = QAction(u'重加载工作区', self)
        reloadWorkspaceAction.triggered.connect(lambda: actions.ActionReloadWorkspace(workspaceName))
        popMenu.addAction(reloadWorkspaceAction)
        removeWorkspaceAction = QAction(u'移除', self)
        removeWorkspaceAction.triggered.connect(lambda: actions.ActionRemoveWorkspace(workspaceName))
        popMenu.addAction(removeWorkspaceAction)
        delWorkspaceAction = QAction(u'删除', self)
        delWorkspaceAction.triggered.connect(lambda: actions.ActionDeleteWorkspace(workspaceName))
        popMenu.addAction(delWorkspaceAction)
        popMenu.addSeparator()

        saveWorkspaceAction = QAction(u'保存工作区', self)
        saveWorkspaceAction.triggered.connect(lambda: actions.ActionSaveWorkspace(workspaceName))
        popMenu.addAction(saveWorkspaceAction)
        saveAsWorkspaceAction = QAction(u'工作区另存为', self)
        saveAsWorkspaceAction.triggered.connect(lambda: actions.ActionSaveAsWorkspace(workspaceName))
        popMenu.addAction(saveAsWorkspaceAction)
        exportWorkspaceAction = QAction(u'导出工作区', self)
        exportWorkspaceAction.triggered.connect(lambda: actions.ActionExportWorkspace(workspaceName))
        popMenu.addAction(exportWorkspaceAction)

        return popMenu

    #右击目录时的菜单
    def _onDirectoryContextMenu(self, modelIndex):
        item = self.treeModel.itemFromIndex(modelIndex)
        workspaceName = item.getWorkspaceName()

        popMenu = QMenu()
        expandAction = QAction(u'展开', self)
        expandAction.triggered.connect(lambda: self._actionExpand(modelIndex))
        popMenu.addAction(expandAction)
        collapseAction = QAction(u'收起', self)
        collapseAction.triggered.connect(lambda: self._actionCollapse(modelIndex))
        popMenu.addAction(collapseAction)
        popMenu.addSeparator()

        newDirAction = QAction(u'新建目录', self)
        newDirAction.triggered.connect(lambda: self._actionNewDirectory(item))
        popMenu.addAction(newDirAction)
        newTreection = QAction(u'新建行为树', self)
        newTreection.triggered.connect(lambda: self._actionNewTree(item))
        popMenu.addAction(newTreection)
        importTeeAction = QAction(u'导入行为树', self)
        importTeeAction.triggered.connect(lambda: self._actionImportTree(item))
        popMenu.addAction(importTeeAction)
        popMenu.addSeparator()
        
        renameDirAction = QAction(u'重命名', self)
        renameDirAction.triggered.connect(lambda: actions.ActionRenameDirectory(item.getPath()))
        popMenu.addAction(renameDirAction)
        delDirAction = QAction(u'删除', self)
        delDirAction.triggered.connect(lambda: actions.ActionDeleteDirectory(item.getPath()))
        popMenu.addAction(delDirAction)

        return popMenu
    
    #右击行为树时的菜单
    def _onTreeContextMenu(self, modelIndex):
        item = self.treeModel.itemFromIndex(modelIndex)
        workspaceName = item.getWorkspaceName()

        popMenu = QMenu()
        saveTreeAction = QAction(u'保存', self)
        saveTreeAction.triggered.connect(lambda: actions.ActionSaveTree(item.getPath()))
        popMenu.addAction(saveTreeAction)
        saveAsTreeAction = QAction(u'另存为', self)
        saveAsTreeAction.triggered.connect(lambda: actions.ActionSaveAsTree(item.getPath()))
        popMenu.addAction(saveAsTreeAction)
        popMenu.addSeparator()
        
        renameTreeAction = QAction(u'重命名', self)
        renameTreeAction.triggered.connect(lambda: actions.ActionRenameTree(item.getPath()))
        popMenu.addAction(renameTreeAction)
        delTreeAction = QAction(u'删除', self)
        delTreeAction.triggered.connect(lambda: actions.ActionDeleteTree(item.getPath()))
        popMenu.addAction(delTreeAction)
        popMenu.addSeparator()

        exportWorkspaceAction = QAction(u'导出', self)
        exportWorkspaceAction.triggered.connect(lambda: actions.ActionExportTree(item.getPath()))
        popMenu.addAction(exportWorkspaceAction)

        return popMenu
    
    def _showContextMenu(self, pos):
        menu = self._simpleContextMenu()
        for _ in range(1):
            qidx, qidx2 = self.currentIndex(), self.indexAt(pos)
            # qidx, qidx2 = qidx.row(), qidx2.row()
            if not qidx.isValid() or not qidx2.isValid():
                break

            item = self.treeModel.itemFromIndex(qidx)
            item2 = self.treeModel.itemFromIndex(qidx2)
            if item == None or item2 == None:
                break
            if item.typ == TreeViewWorkspaceStandardItem.TypeWorkspace:
                menu = self._onWorkspaceContextMenu(qidx)
            elif item.typ == TreeViewWorkspaceStandardItem.TypeDirectory:
                menu = self._onDirectoryContextMenu(qidx)
            if item.typ == TreeViewWorkspaceStandardItem.TypeTree:
                menu = self._onTreeContextMenu(qidx)
        menu.exec(QCursor.pos())
    
    def _actionExpand(self, modelIndex):
        self.expand(modelIndex)
    
    def _actionCollapse(self, modelIndex):
        self.collapse(modelIndex)

    '''
    创建目录
    workspaceName - 工作区
    directory - 父目录
    '''
    def _actionNewDirectory(self, item):
        path = item.getPath()
        pre = '/'.join(path)
        directory = ''
        while True:
            directory = QInputDialog().getText(self, "新建目录", pre+"\n请输入新建目录名：", text=directory)
            if not directory[1] or not directory[0]:
                return
            directory = directory[0]
            if utils.isValidName(directory):
                break
            QMessageBox.warning(view_gg.MainWindow, '错误', '目录名非法', QMessageBox.StandardButton.Yes)
        
        ret = Controller.ModelWorkspaceNewDirectory(path[0], path[1:], directory)
        if ret:
            QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
            return

        subItem = TreeViewWorkspaceStandardItem(item, directory, TreeViewWorkspaceStandardItem.TypeDirectory)
        item.insertRow(0, [subItem])
        self.treeModel.sort(0)
        self.expand(item.index())

    '''
    创建行为树
    item - 右击时的节点
    '''
    def _actionNewTree(self, item):
        path = item.getPath()
        pre = '/'.join(path)
        treeName = ''
        while True:
            treeName = QInputDialog().getText(self, "新建行为树", pre+"\n请输入行为树名：", text=treeName)
            if not treeName[1] or not treeName[0]:
                return
            treeName = treeName[0]
            if utils.isValidName(treeName):
                break
            QMessageBox.warning(view_gg.MainWindow, '错误', '行为树名非法', QMessageBox.StandardButton.Yes)
        
        ret = Controller.ModelWorkspaceNewModel(path[0], path[1:], treeName)
        if ret:
            QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
            return
        
        path.append(treeName)
        self.AddNewTree.emit(path)
        # subItem = TreeViewWorkspaceStandardItem(item, treeName, TreeViewWorkspaceStandardItem.TypeTree)
        # item.insertRow(0, [subItem])
        # self.treeModel.sort(0)
        # self.expand(item.index())

        view_gg.MainWindow.OpenTree.emit(path)

    '''
    创建行为树
    item - 右击时的节点
    '''
    def _actionImportTree(self, item):
        actions.ActionImportTree(item.getPath())

    def onOpenedTreeChanged(self, path):
        # item = self.findWorkspaceItemByName(path[0])
        if self.currentOpenItem:
            self.currentOpenItem.setBackground(QColor(255, 255, 255))
            self.currentOpenItem = None

        item = self.findItemByPath(path, [TreeViewWorkspaceStandardItem.TypeTree])
        if not item:
            return
        
        item.setBackground(DialogSceneSetting.GetColor('TreeViewEditingColor'))
        self.currentOpenItem = item

        parents = self.findParentsByItem(item)
        list(filter(lambda x: self.expand(x.index()), parents))

    def onDoubleClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        if not item or item.typ != TreeViewWorkspaceStandardItem.TypeTree:
            return
        path = item.getPath()
        view_gg.MainWindow.OpenTree.emit(path)

    def onWorkspaceDeleted(self, wsName):
        item = self.findWorkspaceItemByName(wsName)
        if not item:
            return
        tobeRemTreeItem = item.getAllChildren(lambda x: x.typ == TreeViewWorkspaceStandardItem.TypeTree)
        for i in tobeRemTreeItem:
            if self.currentOpenItem == i:
                self.currentOpenItem = None
        tobeRemTreePath = [v.getPath() for v in tobeRemTreeItem]
        for p in tobeRemTreePath:
            view_gg.MainWindow.TreeDeleted.emit(p)
        self.treeModel.removeRow(item.row())

    def onDirectoryDeleted(self, path):
        item = self.findItemByPath(path, [TreeViewWorkspaceStandardItem.TypeDirectory])
        if not item:
            return
        tobeRemTreeItem = item.getAllChildren(lambda x: x.typ == TreeViewWorkspaceStandardItem.TypeTree)
        for i in tobeRemTreeItem:
            if self.currentOpenItem == i:
                self.currentOpenItem = None
        tobeRemTreePath = [v.getPath() for v in tobeRemTreeItem]
        for p in tobeRemTreePath:
            view_gg.MainWindow.TreeDeleted.emit(p)
        self.treeModel.removeRow(item.row(), item.parent().index())

    def onTreeDeleted(self, path):
        item = self.findItemByPath(path, [TreeViewWorkspaceStandardItem.TypeTree])
        if not item:
            return
        if self.currentOpenItem == item:
            self.currentOpenItem = None
        parent = item.parent()
        self.treeModel.removeRow(item.row(), parent.index())
        #可能需要改变父节点的保存状态
        self._checkAndClearUnsaveFlag(parent)
    
    def onSceneSettingChanged(self):
        if not self.currentOpenItem:
            return
        self.currentOpenItem.setBackground(DialogSceneSetting.GetColor('TreeViewEditingColor'))
    
    #对给定节点item，逐级往上检查每层节点，如果某节点的所有子节点都已保存，则清掉未保存标记
    def _checkAndClearUnsaveFlag(self, item):
        parents = self.findParentsByItem(item)
        parents.insert(0, item)
        for p in parents:
            if p.countFirstLevelChildren(lambda x: not x.isSaved()) > 0:
                break
            p.setSavedFlag(True)
    
    def onTreeChanged(self, path: list, saved: bool):
        item = self.findItemByPath(path, [TreeViewWorkspaceStandardItem.TypeTree])
        if not item:
            return
        item.setSavedFlag(saved)

        if saved:
            #如果行为树保存了，则往上逐级检查，对于子节点都保存的节点，清掉未保存标记
            self._checkAndClearUnsaveFlag(item)
        else:
            parents = self.findParentsByItem(item)
            list(filter(lambda x: x.setSavedFlag(saved), parents))
    
    #对item以及它的所有递归子节点执行func操作
    def doOnItemAndSuccessor(self, item, func):
        items = item.getAllChildren()
        for v in items:
            func(v)
    
    #工作区保存信号反馈
    def onWorkspaceSaved(self, wsName):
        item = self.findWorkspaceItemByName(wsName)
        if not item:
            return
        def func(x):
            x.setSavedFlag(True)
        #清掉所有未保存标记
        self.doOnItemAndSuccessor(item, func)
    
    def _addTreeItemByViewData(self, parentItem, data):
        item = TreeViewWorkspaceStandardItem(None, data, TreeViewWorkspaceStandardItem.TypeTree)
        parentItem.insertRow(0, [item])

    def _addDirItemByViewData(self, parentItem, data, depth):
        item = TreeViewWorkspaceStandardItem(None, data['name'],
            TreeViewWorkspaceStandardItem.TypeWorkspace if depth == 0 else TreeViewWorkspaceStandardItem.TypeDirectory)
        parentItem.insertRow(0, [item])
        for t in data['trees']:
            self._addTreeItemByViewData(item, t)
        for d in data['dirs']:
            self._addDirItemByViewData(item, d, depth+1)
    
    def addWorkspaceByViewData(self, data):
        self._addDirItemByViewData(self.rootNode, data, 0)
        self.treeModel.sort(0)
    
    #返回未保存的工作区列表
    def getUnsavedWorkspaces(self) -> list:
        ret = []
        for i in range(self.rootNode.rowCount()):
            child = self.rootNode.child(i)
            if not child.isSaved():
                ret.append(child.name)
        return ret
