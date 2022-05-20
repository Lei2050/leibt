import os
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog

import view.dialog_new_workspace as dialog_new_workspace
import view.dialog_export as dialog_export
import view.dialog_scene_setting as dialog_scene_setting
import g.gg as gg
from g.config import Config
import view.gg as view_gg
import common.utils as utils
from controller.controller import Controller

'''
供视图层全局调用的action反应函数
'''

def ActionAfterMainWindowSetuped():
    openWorkspaces = Config().loadOpenWorkspaces()
    #这里先获取Config().loadCurrentEditTree()，因为下面执行打开行为树时可能会覆盖loadCurrentEditTree()的值
    currentTree = Config().loadCurrentEditTree()
    for k, v in openWorkspaces.items():
        wsFilename = v['directory'].rstrip('/\\') + '/' + k + gg.WorkspaceFileSubfix
        ret = Controller.ModelOpenWorkspace(wsFilename)
        if ret:
            QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
            return
    
    openTrees = Config().loadOpenTrees()
    for k in openTrees.keys():
        path = gg.getPathFromStr(k)
        modelData = Controller.GetModel(path)
        if not modelData:
            continue
        view_gg.MainWindow.OpenTree.emit(path)

    path = gg.getPathFromStr(currentTree)
    view_gg.MainWindow.OpenTree.emit(path)

#将某个工作区加入到软件配置中，下次软件启动的时候就直接打开了
def ActionAddWorkspaceIntoCONFIG(wsName):
    workspace = Controller.ModelGetWorkspace(wsName)
    params = workspace.copy()
    Config().addWorkspace(wsName, {'directory':params['directory']})

#新建工作区
def ActionNewWorkspace():
    workspaceName = None
    params = {}
    while True:
        dialog = dialog_new_workspace.DialogNewWorkspace(view_gg.MainWindow, params)
        if dialog.exec():
            params = dialog.getParams()
            name, directory, exportDir = params['name'], params['directory'], params['export_directory']
            ret = Controller.ModelNewWorkspace(name, directory, exportDir)
            if ret:
                QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
            else:
                workspaceName = name
                break
        else:
            return
    view_gg.WorkspaceTreeView.NewWorkspace.emit(workspaceName)

    ActionAddWorkspaceIntoCONFIG(workspaceName)

#编辑工作区
def ActionEditWorkspace(workspaceName):
    workspace = Controller.ModelGetWorkspace(workspaceName)
    params = workspace.copy()
    while True:
        dialog = dialog_new_workspace.DialogNewWorkspace(view_gg.MainWindow, params)
        dialog.unableChooseDirectory()
        dialog.setWindowTitle('编辑工作区')
        if dialog.exec():
            params = dialog.getParams()
            ret = Controller.ModelEditWorkspace(workspace, params)
            if ret:
                QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
            else:
                break
        else:
            return
    if workspaceName != params['name']:
        view_gg.MainWindow.WorkspaceRenamed.emit(workspaceName, params['name'])
    QMessageBox.information(view_gg.MainWindow, '提示', 'OK', QMessageBox.StandardButton.Yes)

#重载工作区
def ActionReloadWorkspace(workspaceName):
    workspace = Controller.ModelGetWorkspace(workspaceName)
    params = workspace.copy()
    #先直接移除
    ActionRemoveWorkspace(workspaceName)
    #然后加载
    wsFilename = params['directory'].lstrip('/\\') + '/' + workspaceName + gg.WorkspaceFileSubfix
    ret = Controller.ModelOpenWorkspace(wsFilename)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return

#移除工作区
def ActionRemoveWorkspace(workspaceName):
    Controller.ModelRemoveWorkspace(workspaceName)
    view_gg.MainWindow.WorkspaceDeleted.emit(workspaceName)
    Config().remWorkspace(workspaceName)

#保存工作区
def ActionSaveWorkspace(workspaceName):
    ret = Controller.ModelSaveWorkspace(workspaceName)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    QMessageBox.information(view_gg.MainWindow, '提示', 'OK', QMessageBox.StandardButton.Yes)
    view_gg.WorkspaceTreeView.WorkspaceSaved.emit(workspaceName)

#导入行为树
def ActionImportTree(prePath):
    filepath = QFileDialog.getOpenFileName(view_gg.MainWindow, "请选择导入文件", "/", f"Tree Files (*{gg.TreeFileSubfix})")
    filepath = filepath[0]
    if not filepath:
        return

    ret = Controller.ModelImportModel(prePath, filepath)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    
    _, tail = os.path.split(filepath)
    name = tail.split('.')[0]
    path = prePath + [name]
    view_gg.WorkspaceTreeView.AddNewTree.emit(path)
    view_gg.MainWindow.OpenTree.emit(path)

#删除工作区
def ActionDeleteWorkspace(wsName):
    reply = QMessageBox.question(view_gg.MainWindow, 'Warning',
        f"确认删除工作区({wsName})？", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
    if reply != QMessageBox.StandardButton.Yes:
        return

    ret = Controller.ModelDeleteWorkspace(wsName)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    
    view_gg.MainWindow.WorkspaceDeleted.emit(wsName)

    Config().remWorkspace(wsName)

#重命名目录
def ActionRenameDirectory(path):
    title = u'重命名目录：' + gg.getPathFromList(path)
    dirName = None
    while True:
        dirName = QInputDialog().getText(view_gg.MainWindow, title, u"请输入新的目录名：", text=path[-1])
        if not dirName[1] or not dirName[0]:
            return
        dirName = dirName[0]
        if utils.isValidName(dirName):
            break
        QMessageBox.warning(view_gg.MainWindow, '错误', '目录名非法', QMessageBox.StandardButton.Yes)
    
    ret = Controller.ModelRenameDirectory(path, dirName)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return

    view_gg.MainWindow.DirRenamed.emit(path, dirName)

#重命名行为树
def ActionRenameTree(path):
    title = u'重命名行为树：' + gg.getPathFromList(path)
    treeName = None
    while True:
        treeName = QInputDialog().getText(view_gg.MainWindow, title, u"请输入新的行为树名：", text=path[-1])
        if not treeName[1] or not treeName[0]:
            return
        treeName = treeName[0]
        if utils.isValidName(treeName):
            break
        QMessageBox.warning(view_gg.MainWindow, '错误', '行为树名非法', QMessageBox.StandardButton.Yes)
    
    ret = Controller.ModelRenameTree(path, treeName)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return

    view_gg.MainWindow.TreeRenamed.emit(path, treeName)

#删除指定目录
#path - 从工作区到该目录的相对路径
#比如，删除工作区mu下a目录下的b目录，则path = [mu, a, b]
def ActionDeleteDirectory(path):
    key = gg.getKeyFromPath(path)
    reply = QMessageBox.question(view_gg.MainWindow, 'Warning',
        f"确认删除目录({key})？", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
    if reply != QMessageBox.StandardButton.Yes:
        return

    ret = Controller.ModelDeleteDirectory(path)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    
    view_gg.MainWindow.DirectoryDeleted.emit(path)

#删除指定行为树
#path - 从工作区到该行为树的相对路径
#比如，删除工作区mu下行为树a/b/t，则path = [mu, a, b, t]
def ActionDeleteTree(path):
    key = gg.getKeyFromPath(path)
    reply = QMessageBox.question(view_gg.MainWindow, 'Warning',
        f"确认删除行为树({key})？", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
    if reply != QMessageBox.StandardButton.Yes:
        return

    ret = Controller.ModelDeleteTree(path)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    
    view_gg.MainWindow.TreeDeleted.emit(path)

#工作区另存为
def ActionSaveAsWorkspace(wsName):
    directory = QFileDialog.getExistingDirectory(view_gg.MainWindow, "请选择目录", "/")
    if not directory:
        return

    ret = Controller.ModelSaveAsWorkspace(wsName, directory)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    
    QMessageBox.information(view_gg.MainWindow, '提示', 'OK', QMessageBox.StandardButton.Yes)
    
    ActionAddWorkspaceIntoCONFIG(wsName)

#选择并打开一个工作区
def ActionOpenWorkspace():
    filepath = QFileDialog.getOpenFileName(view_gg.MainWindow, "请选择文件", "/", f"Workspace Files (*{gg.WorkspaceFileSubfix})")
    filepath = filepath[0]
    if not filepath:
        return

    ret = Controller.ModelOpenWorkspace(filepath)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return

#工作区已打开通知
def ActionWorkspaceOpened(wsName):
    ret = Controller.ModelGetWorkspaceViewData(wsName)
    if isinstance(ret, str):
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    view_gg.WorkspaceTreeView.addWorkspaceByViewData(ret)
    
    ActionAddWorkspaceIntoCONFIG(wsName)

#导出工作区（生成代码）
def ActionExportWorkspace(wsName):
    workspace = Controller.ModelGetWorkspace(wsName)
    if not workspace:
        return
    params = workspace.copy()

    #执行导出之前先保存行为树
    Controller.ModelSaveWorkspace(wsName)
    view_gg.ClearInfoPlainTextEdit()

    dialog = dialog_export.DialogExport(view_gg.MainWindow, params)
    if not dialog.exec():
        return
    params = dialog.getParams()
    ret = Controller.ModelExportWorkspace(wsName, params['export_directory'])
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    
    QMessageBox.information(view_gg.MainWindow, '提示', '导出成功', QMessageBox.StandardButton.Yes)

#导出某棵行为树（生成代码）
def ActionExportTree(path):
    workspace = Controller.ModelGetWorkspace(path[0])
    if not workspace:
        return
    params = workspace.copy()

    #执行导出之前先保存行为树
    Controller.ModelSaveWorkspace(path[0])
    view_gg.ClearInfoPlainTextEdit()

    dialog = dialog_export.DialogExport(view_gg.MainWindow, params)
    if not dialog.exec():
        return
    params = dialog.getParams()
    ret = Controller.ModelExportTree(path, params['export_directory'])
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    
    QMessageBox.information(view_gg.MainWindow, '提示', '导出成功', QMessageBox.StandardButton.Yes)

#保存一棵行为树
def ActionSaveTree(path):
    ret = Controller.ModelSaveTree(path)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    view_gg.InfoPlainTextEditAppenText(gg.getPathFromList(path) + '保存成功')

#另存为一棵行为树
def ActionSaveAsTree(path):
    directory = QFileDialog.getExistingDirectory(view_gg.MainWindow, "请选择目录", "/")
    if not directory:
        return
    ret = Controller.ModelSaveAsTree(path, directory)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    view_gg.InfoPlainTextEditAppenText(gg.getPathFromList(path) + '另存成功')

#复制一个节点（包含了它的所有后继），
#path - 行为树
#itemId - 节点id
def ActionCopyModelItem(path, itemId):
    ret = Controller.ModelCopyModelItem(path, itemId)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    view_gg.InfoPlainTextEditAppenText(f'已复制节点{itemId}')

#将复制的节点粘贴到其他节点上，
#path - 行为树
#itemId - 节点id
def ActionPasteModelItem(path, itemId):
    ret = Controller.ModelPasteModelItem(path, itemId)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return

#复制一个节点（包含了它的所有后继），
#path - 行为树
#itemId - 节点id
def ActionCutModelItem(path, itemId):
    ret = Controller.ModelCopyModelItem(path, itemId)
    if ret:
        QMessageBox.warning(view_gg.MainWindow, '错误', ret, QMessageBox.StandardButton.Yes)
        return
    Controller.CmdDelete(path, itemId)

def ActionSceneSetting():
    if dialog_scene_setting.Instance:
        #已经有对话框打开
        return
    dialog = dialog_scene_setting.DialogSceneSetting(view_gg.MainWindow)
    dialog.show()
