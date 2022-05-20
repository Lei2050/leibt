from PyQt6.QtWidgets import QTabWidget

import g.gg as gg
from g.config import Config
import view.gg as view_gg
from view.widget_scene import WidgetScene

class TabWidgetScene(QTabWidget):
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)

        #<str_path, WidgetScene>
        self.sceneWidgets = {}

        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)

        self.currentChanged.connect(self._onCurrentChanged)
        self.tabCloseRequested.connect(self.onCloseTab)
        view_gg.MainWindow.OpenTree.connect(self.onTreeOpen)
        view_gg.MainWindow.TreeDeleted.connect(self.onTreeDeleted)
        view_gg.MainWindow.SceneSettingChanged.connect(self.onSceneSettingChanged)
        view_gg.MainWindow.TreeChanged.connect(self.onTreeChanged)
        view_gg.MainWindow.WorkspaceSaved.connect(self.onWorkspaceSaved)
        view_gg.MainWindow.WorkspaceRenamed.connect(self.onWorkspaceRenamed)
        view_gg.MainWindow.DirRenamed.connect(self.onDirRenamed)
        view_gg.MainWindow.TreeRenamed.connect(self.onTreeRenamed)

    def getWidgetScene(self, path):
        key = gg.getKeyFromPath(path)
        return self.sceneWidgets.get(key, None)

    # def keyPressEvent(self, keyEvent):
    #     super(TabWidgetScene, self).keyPressEvent(keyEvent)
    #     print('hdfwefoe')

    #     keyEvent.accept()

    def _onCurrentChanged(self, int):
        widgetScene = self.currentWidget()
        if widgetScene:
            view_gg.MainWindow.ViewSceneChanged.emit(widgetScene.modelPath)
        else:
            view_gg.MainWindow.ViewSceneChanged.emit([])
        self._saveCurrentEditTreeCfg()
    
    def _saveCurrentEditTreeCfg(self):
        widget = self.currentWidget()
        if widget:
            key = gg.getKeyFromPath(widget.modelPath)
            Config().saveCurrentEditTree(key)
        else:
            Config().saveCurrentEditTree('')
    
    def onKeyPress(self, keyEvent):
        widgetScene = self.currentWidget()
        if widgetScene:
            widgetScene.onKeyPress(keyEvent)

    def onTreeOpen(self, path):
        if len(path) < 2:
            #具体到行为树，path必定>=2，至少是工作区名和自己的名字
            return
        key = gg.getKeyFromPath(path)
        widget = self.sceneWidgets.get(key, None)
        if not widget:
            widget = WidgetScene(path)
            self.sceneWidgets[key] = widget
            # self.addTab(widget)
            # self.insertTab(self.currentIndex(), widget, path[-1])
            self.insertTab(self.currentIndex()+1, widget, key)
            Config().saveTreeCfg(key, {})
        self.setCurrentWidget(widget)
        # self._saveCurrentEditTreeCfg()
    
    def onTreeDeleted(self, path):
        if len(path) < 2:
            #具体到行为树，path必定>=2，至少是工作区名和自己的名字
            return
        key = gg.getKeyFromPath(path)
        widget = self.sceneWidgets.pop(key, None)
        if widget:
            self.removeTab(self.indexOf(widget))
            Config().remTreeCfg(key)

    def onCloseTab(self, index):
        widget = self.widget(index)
        if widget:
            key = gg.getKeyFromPath(widget.modelPath)
            self.sceneWidgets.pop(key, None)
            widget.onCloseScene()
        self.removeTab(index)
        
        # self._saveCurrentEditTreeCfg()
    
    def onSceneSettingChanged(self):
        widget = self.currentWidget()
        if not widget:
            return
        widget.repaintTree()
    
    def _setSavedFlag(self, widget, saved: bool):
        tabName = gg.getKeyFromPath(widget.modelPath)
        self.setTabText(self.indexOf(widget), tabName + ('' if saved else ' *'))
    
    def onTreeChanged(self, path: list, saved: bool):
        widget = self.getWidgetScene(path)
        if not widget:
            return
        self._setSavedFlag(widget, saved)
    
    def onWorkspaceSaved(self, wsName):
        for i in range(self.count()):
            widget = self.widget(i)
            self._setSavedFlag(widget, True)
    
    def _saveOpenedTreesMemory(self):
        Config().removeAllOpenTree()
        for i in range(self.count()):
            widget = self.widget(i)
            widget.saveConfigToDisk()
            if widget == self.currentWidget():
                Config().saveCurrentEditTree(gg.getKeyFromPath(widget.modelPath))
        Config().save(force=True)

    def _widgetSetModelpath(self, widget, modelPath):
        key = gg.getKeyFromPath(widget.modelPath)
        self.sceneWidgets.pop(key, None)

        widget.setModelPath(modelPath)

        key = gg.getKeyFromPath(widget.modelPath)
        self.sceneWidgets[key] = widget

        index = self.indexOf(widget)
        tabText = self.tabText(index)
        saved = not tabText.endswith('*')
        self._setSavedFlag(widget, saved)

    def onWorkspaceRenamed(self, oldName, newName):
        for i in range(self.count()):
            widget = self.widget(i)
            if widget.modelPath[0] != oldName:
                continue
            newModelPath = widget.modelPath.copy()
            newModelPath[0] = newName
            self._widgetSetModelpath(widget, newModelPath)
        self._saveOpenedTreesMemory()
    
    def onDirRenamed(self, path, newName):
        for i in range(self.count()):
            widget = self.widget(i)
            if len(widget.modelPath) <= len(path) or widget.modelPath[:len(path)] != path:
                continue
            newModelPath = widget.modelPath.copy()
            newModelPath[len(path)-1] = newName
            self._widgetSetModelpath(widget, newModelPath)
        self._saveOpenedTreesMemory()
    
    def onTreeRenamed(self, path, newName):
        path = path.copy()
        Config().remTreeCfg(path)
        widget = self.getWidgetScene(path)
        if not widget:
            return
        newModelPath = widget.modelPath.copy()
        newModelPath[-1] = newName
        self._widgetSetModelpath(widget, newModelPath)
        widget.saveConfigToDisk()
        Config().save(force=True)
