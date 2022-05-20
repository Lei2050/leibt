import model.workspace as mws

import view.gg as view_gg

class Controller:
    def __init__(self):
        pass
    
    #根据路径获取行为树实体
    @classmethod
    def GetModel(cls, path):
        return mws.WorkspaceMgr().getModelByPath(path)
    
    '''
    获取给定数据模型的节点的属性数据
    '''
    @classmethod
    def GetModelItemData(cls, path, itemId):
        item = cls.GetModel(path).getItem(itemId)
        if item:
            return item.getData()
        return None
    
    '''
    更新给定数据模型的节点的属性数据
    '''
    @classmethod
    def UpdateModelItemData(cls, path, itemId, data):
        model = cls.GetModel(path)
        if not model:
            return
        item = model.getItem(itemId)
        if not item:
            return

        if item.updateData(data):
            #向视图层发通知，数据有变更且未保存
            view_gg.MainWindow.TreeChanged.emit(path, False)
    
    '''
    通知视图层行为树数据有变更
    '''
    @classmethod
    def ViewTreeChanged(cls, path: list, saved: bool):
        view_gg.MainWindow.TreeChanged.emit(path, saved)

    @classmethod
    def Redo(cls, path):
        ret = cls.GetModel(path).redo()
        if ret:
            view_gg.MainWindow.TreeChanged.emit(path, False)
        return ret

    @classmethod
    def Undo(cls, path):
        ret = cls.GetModel(path).undo()
        if ret:
            view_gg.MainWindow.TreeChanged.emit(path, False)
        return ret
    
    '''
    k - model的key
    导出指定行为树
    '''
    @classmethod
    def ExportModel(cls, path):
        cls.GetModel(path).export()
    
    '''
    k - model的key
    pItemId - 父节点的id
    idx - 插入的位置
    itemType - 插入的节点类型
    successorItemId - 后继节点的id，如果该值>0，则是在pItemId和successorItemId之间插入
    '''
    @classmethod
    def CmdAddItemByIdAndType(cls, k, pItemId, itemType, idx):
        cls.GetModel(k).cmdAddItemByIdAndType(pItemId, itemType, idx)
    
    @classmethod
    def CmdAppendItem(cls, k, itemId, itemType):
        cls.GetModel(k).cmdAppendItem(itemId, itemType)

    '''
    在节点itemId前面插入类型为itemType的节点
    '''
    @classmethod
    def CmdInsertItemBefore(cls, k, itemId, itemType):
        cls.GetModel(k).CmdInsertItemBefore(itemId, itemType)
    
    @classmethod
    def CmdInsertItemPreSibling(cls, k, itemId, itemType):
        cls.GetModel(k).CmdInsertItemPreSibling(itemId, itemType)
    
    @classmethod
    def CmdInsertItemNextSibling(cls, k, itemId, itemType):
        cls.GetModel(k).CmdInsertItemNextSibling(itemId, itemType)
    
    @classmethod
    def CmdReplaceItem(cls, k, itemId, itemType):
        cls.GetModel(k).CmdReplaceItem(itemId, itemType)

    @classmethod
    def CmdReplaceNonfixedChildCombinationItem(cls, k, itemId, itemType):
        cls.GetModel(k).CmdReplaceNonfixedChildCombinationItem(itemId, itemType)
    
    @classmethod
    def CmdDelete(cls, k, itemId):
        cls.GetModel(k).CmdDelete(itemId)
    
    '''
    跟兄弟节点交换位置
    upOrDown = true - 跟上交换；false - 跟下节点交换
    '''
    @classmethod
    def CmdSwapSibling(cls, k, itemId, upOrDown):
        cls.GetModel(k).CmdSwapSibling(itemId, upOrDown)
    
    '''
    return：str - 错误信息；None - 成功
    '''
    @classmethod
    def ModelNewWorkspace(cls, name, directory, exportDirectory):
        return mws.NewWorkspace(name, directory, exportDirectory)
    
    '''
    获取工作区的数据，注意返回的不是model的实体，而是相关数据
    return：dict
    '''
    @classmethod
    def ModelGetWorkspace(cls, name):
        return mws.GetWorkspace(name)

    '''
    在指定工作区中创建目录
    wsName - str - 工作区名字
    parentPath - list - 目录父目录路径
    directory - str - 新目录名
    '''
    @classmethod
    def ModelWorkspaceNewDirectory(cls, wsName, parentPath, directory):
        return mws.WorkspaceNewDirectory(wsName, parentPath, directory)

    '''
    在指定工作区中创建行为树
    wsName - str - 工作区名字
    parentPath - list - 目录父目录路径
    directory - str - 新目录名
    '''
    @classmethod
    def ModelWorkspaceNewModel(cls, wsName, parentPath, treeName):
        return mws.WorkspaceNewModel(wsName, parentPath, treeName)

    '''
    编辑工作区
    oldData - {} - 老的工作区数据
    newData - {} - 新的工作区数据
    '''
    @classmethod
    def ModelEditWorkspace(cls, oldData, newData):
        return mws.EditWorkspace(oldData, newData)
        
    '''
    移除工作区
    '''
    @classmethod
    def ModelRemoveWorkspace(cls, workspaceName):
        return mws.RemoveWorkspace(workspaceName)
        
    '''
    保存工作区
    '''
    @classmethod
    def ModelSaveWorkspace(cls, wsName):
        ret = mws.SaveWorkspace(wsName)
        if not ret:
            view_gg.MainWindow.WorkspaceSaved.emit(wsName)
        return ret
    
    '''
    导入行为树
    '''
    @classmethod
    def ModelImportModel(cls, path, filepath):
        return mws.ImportModel(path, filepath)
    
    '''
    删除工作区
    '''
    @classmethod
    def ModelDeleteWorkspace(cls, wsName):
        return mws.DeleteWorkspace(wsName)
    
    '''
    删除目录
    '''
    @classmethod
    def ModelDeleteDirectory(cls, wsName):
        return mws.DeleteDirectory(wsName)

    '''
    删除行为树
    '''
    @classmethod
    def ModelDeleteTree(cls, path):
        return mws.DeleteTree(path)

    '''
    另存工作区
    '''
    @classmethod
    def ModelSaveAsWorkspace(cls, wsName, newDirectory):
        ret = mws.SaveAsWorkspace(wsName, newDirectory)
        if not ret:
            view_gg.MainWindow.WorkspaceSaved.emit(wsName)
        return ret
        
    '''
    打开工作区
    '''
    @classmethod
    def ModelOpenWorkspace(cls, filepath):
        return mws.OpenWorkspace(filepath)
    
    '''
    获取工作区在视图层中的展示数据
    '''
    @classmethod
    def ModelGetWorkspaceViewData(cls, wsName):
        return mws.GetWorkspaceViewData(wsName)
    
    '''
    导出整个工作区为代码
    directory - 导出到目录
    '''
    @classmethod
    def ModelExportWorkspace(cls, wsName, exportDirectory):
        return mws.ExportWorkspace(wsName, exportDirectory)
    
    '''
    导出某棵行为树为代码
    directory - 导出到目录
    '''
    @classmethod
    def ModelExportTree(cls, path, exportDirectory):
        return mws.ExportTree(path, exportDirectory)
        
    '''
    获取给定空间的所有行为树，返回这些行为的路径的列表
    '''
    @classmethod
    def ModelGetAllModelPaths(cls, wsName):
        return mws.GetAllModelPaths(wsName)
        
    '''
    指定行为树，执行错误检查，返回错误信息
    '''
    @classmethod
    def ModelCheckModelError(cls, path):
        return mws.CheckModelError(path)
    
    '''
    保存指定行为树
    '''
    @classmethod
    def ModelSaveTree(cls, path):
        ret = mws.SaveTree(path)
        if not ret:
            view_gg.MainWindow.TreeChanged.emit(path, True)
        return ret
    
    '''
    保存指定行为树
    '''
    @classmethod
    def ModelSaveAsTree(cls, path, directory):
        ret = mws.SaveAsTree(path, directory)
        if not ret:
            view_gg.MainWindow.TreeChanged.emit(path, True)
        return ret
    
    '''
    复制一个节点（包含了它的所有后继），
    path - 行为树
    id - 节点id
    '''
    @classmethod
    def ModelCopyModelItem(cls, path, id):
        return mws.CopyModelItem(path, id)
        
    '''
    复制一个节点（包含了它的所有后继），
    path - 行为树
    id - 被覆盖的节点id
    '''
    @classmethod
    def ModelPasteModelItem(cls, path, id):
        return mws.PasteModelItem(path, id)
        
    '''
    复制一个节点（包含了它的所有后继），
    path - 行为树
    id - 被覆盖的节点id
    '''
    @classmethod
    def ModelSetModelSaved(cls, path, saved: bool):
        cls.GetModel(path).setSaved(saved)
    
    '''
    重命名目录
    oldPath 老的工作区数据
    newData 新的工作区数据
    '''
    @classmethod
    def ModelRenameDirectory(cls, oldPath: list, newName: str):
        return mws.RenameDirectory(oldPath, newName)
    
    '''
    重命名行为树
    oldPath 老的工作区数据
    newData 新的工作区数据
    '''
    @classmethod
    def ModelRenameTree(cls, oldPath: list, newName: str):
        return mws.RenameTree(oldPath, newName)
    
    # @classmethod
    # def ShowViewErrors(cls, k, errors):
    #     view_gg.SceneTabWidget.getWidgetScene(k).showErrors(errors)

    @classmethod
    def ShowViewInfo(cls, info):
        view_gg.InfoPlainTextEditAppenText(info)

    @classmethod
    def ClearViewInfo(cls):
        view_gg.ClearInfoPlainTextEdit()

    @classmethod
    def ViewShowErrorMsgDialog(cls, info):
        view_gg.ShowErrorMsgDialog(info)

    @classmethod
    def ViewWorkspaceOpened(cls, wsName):
        view_gg.MainWindow.WorkspaceOpened.emit(wsName)
    