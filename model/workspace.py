import json
import os
import shutil
import logging

import common.utils as utils
import g.gg as gg
import model.model as mmodel

CNT = gg.ControlNodeType

#类似目录结构的节点
#在视图层要目录结构的组织方式
class WorkspaceItem:
    # TypeDirectory = 1 #目录
    # TypeFile = 2 #文件
    
    def __init__(self, name):
        self.name = name
        # self.type = type
        # key = name, value = WorkspaceItem
    def addDirectory(self, name):
        return False
    
    #path - 在工作区中的完整路径，包括工作空间
    def addModel(self, path, model):
        return False

    #path - 在工作区中的完整路径，包括工作空间
    def newModel(self, path):
        return False
    
    def save(self, path):
        return True

class WorkspaceItemDirectory(WorkspaceItem):
    def __init__(self, name):
        WorkspaceItem.__init__(self, name)
        # self.type = WorkspaceItem.TypeDirectory
        # key = name, value = WorkspaceItem
        self.trees = {}
        self.directory = {}
    
    def addDirectory(self, name):
        if name in self.directory:
            return False
        item = WorkspaceItemDirectory(name)
        self.directory[name] = item
        return item
    
    def remDirectory(self, dirName):
        self.directory.pop(dirName, None)
    
    #model - 行为树实体
    def addModel(self, path, model):
        name = path[-1]
        if not model or name in self.trees:
            return False
        item = WorkspaceItemFile(path, model)
        self.trees[name] = item
        return item

    def newModel(self, path):
        name = path[-1]
        if name in self.trees:
            return False
        item = WorkspaceItemFile(path, None)
        self.trees[name] = item
        return item
    
    def remModel(self, modelName):
        self.trees.pop(modelName, None)
    
    def getDirectory(self, path):
        item = self
        for v in path:
            item = item.directory.get(v, None)
            if not item or not isinstance(item, WorkspaceItemDirectory):
                return None
        return item 
    
    def getModel(self, path, name):
        item = self
        for v in path:
            item = item.directory.get(v, None)
            if not item or not isinstance(item, WorkspaceItemDirectory):
                return None
        item = item.trees.get(name, None)
        if not item or not isinstance(item, WorkspaceItemFile):
            return None
        return item
    
    def saveData(self):
        return {
            'name': self.name,
            'is_dir': True,
            'tree_files': [v.saveData() for v in self.trees.values()],
            'dirs': [v.saveData() for v in self.directory.values()],
        }
    
    def save(self, path):
        path = path + self.name + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        ret = True
        for _, tree in self.trees.items():
            ret = tree.save(path) and ret
        for _, dir in self.directory.items():
            ret = dir.save(path) and ret
        return ret
    
    #wsDirectory - 工作区所在目录
    #path - 相对于工作区的目录路径，包含工作区名，不包含自己
    def load(self, wsDirectory, path, data):
        self.name = data['name']
        path = path + [self.name]
        for d in data['dirs']:
            di = self.addDirectory(d['name'])
            di.load(wsDirectory, path, d)
        for tf in data['tree_files']:
            tpath = path + [tf]
            fi = self.newModel(tpath)
            fi.load(wsDirectory, path, tf)
    
    #获取视图层展示的数据
    def viewData(self):
        return {
            'name': self.name,
            'trees': [v.viewData() for v in self.trees.values()],
            'dirs': [v.viewData() for v in self.directory.values()],
        }
    
    def export(self, exportDirectory):
        errs = []
        for _, tree in self.trees.items():
            ret = tree.export(exportDirectory)
            if ret is not None:
                errs = errs + ret
        for _, dir in self.directory.items():
            ret = dir.export(exportDirectory)
            errs = errs + ret
        return errs
    
    def getAllModelPaths(self, path):
        ret = []
        path = path + [self.name]
        for _, tree in self.trees.items():
            ret = ret + tree.getAllModelPaths(path)
        for _, dir in self.directory.items():
            ret = ret + dir.getAllModelPaths(path)
        return ret
        
    def onWorkspaceRename(self, oldName, newName):
        for _, tree in self.trees.items():
            tree.onWorkspaceRename(oldName, newName)
        for _, dir in self.directory.items():
            dir.onWorkspaceRename(oldName, newName)
    
    #重新更改该目录下的所有目录和行为树的路径
    def resetPath(self, prePath):
        path = prePath + [self.name]
        for _, tree in self.trees.items():
            tree.resetPath(path)
        for _, dir in self.directory.items():
            dir.resetPath(path)

class WorkspaceItemFile(WorkspaceItem):
    def __init__(self, path, model = None):
        name = path[-1]
        WorkspaceItem.__init__(self, name)
        # self.type = WorkspaceItem.TypeDirectory
        # key = name, value = WorkspaceItem
        self.model = model
        if not self.model:
            key = gg.getKeyFromPath(path)
            self.model = mmodel.Model(key)
    
    def saveData(self):
        return self.name
    
    def save(self, path):
        filepath = path + self.name + gg.TreeFileSubfix
        with open(filepath, "w+", encoding='utf-8') as f:
            saveData = self.model.save()
            json.dump(saveData, f, sort_keys=True, indent=4)
        self.model.saved = True
        return True
    
    def load(self, wsDirectory, path, data):
        self.name = data
        prepath = gg.getPathFromList(path)
        filepath = wsDirectory + '/' + prepath + '/' + self.name + gg.TreeFileSubfix
        with open(filepath, "r", encoding='utf-8') as f:
            data = json.load(f)
            if not self.model.load(data):
                raise Exception(gg.ErrorCode.getErrorMsg(14, path=filepath))
    
    #获取视图层展示的数据
    def viewData(self):
        return self.name
    
    def export(self, exportDirectory):
        return self.model.export(exportDirectory)
    
    def getAllModelPaths(self, path):
        return [path + [self.name]]
    
    def onWorkspaceRename(self, oldName, newName):
        path = gg.getPathFromStr(self.model.id)
        path[0] = newName
        self.model.id = gg.getKeyFromPath(path)
        
    #重新更改该行为树的路径
    def resetPath(self, prePath):
        path = prePath + [self.name]
        self.model.id = gg.getKeyFromPath(path)

class Workspace:
    def __init__(self, name, directory, exportDirectory):
        #<name, model>，行为树名 - 行为树
        self.name = name
        self.directory = directory
        self.exportDirectory = exportDirectory
        self.root = WorkspaceItemDirectory(self.name)
    
    def getSaveFilePath(self):
        return self.directory + '/' + self.name + gg.WorkspaceFileSubfix
    
    def saveData(self):
        data = {
            'name': self.name,
            #'directory': self.directory,
            'export_dir': self.exportDirectory,
            'trees': self.root.saveData(),
        }
        return data
    
    #保存工作区文件，并不保存其中的行为树文件
    def saveWorkspaceFile(self):
        filepath = self.getSaveFilePath()
        #调用层处理error
        with open(filepath, "w+", encoding='utf-8') as f:
            json.dump(self.saveData(), f, sort_keys=True, indent=4)
    
    #同时保存工作区文件和其中的行为树文件
    def save(self):
        self.saveWorkspaceFile()
        self.root.save(self.directory + '/')
        return True
    
    def load(self, data):
        self.name = data['name']
        #self.directory = data['directory']
        #self.exportDirectory = data['export_dir']
        d = WorkspaceItemDirectory(None)
        d.load(self.directory, [], data['trees'])
        self.root = d
    
    #获取视图层展示的数据
    def viewData(self):
        data = self.root.viewData()
        data['name'] = self.name
        return data
    
    def getTreeRootDir(self):
        return self.directory + '/' + self.name + '/'
    
    def deleteAllFiles(self):
        file = self.getSaveFilePath()
        if os.path.exists(file):
            os.remove(file)
        # os.rmdir(self.directory + '/' + self.name)
        shutil.rmtree(self.directory + '/' + self.name)
    
    def getDirectoryItem(self, path):
        return self.root.getDirectory(path)
    
    def getModelItem(self, path, modelName):
        return self.root.getModel(path, modelName)
    
    def getModelItemByPath(self, path):
        return self.root.getModel(path[:-1], path[-1])
    
    def export(self, exportDirectory):
        ##这个目录运行行为树代码的必备的库
        ##目前使用Pyinstaller打包，gg.ROOT目录不能正常使用，暂时靠手动拷贝吧。
        # srcDir = gg.ROOT + '/btpy'
        # distDir = exportDirectory + '/btpy'
        # if os.path.exists(distDir):
        #     shutil.rmtree(distDir)
        # shutil.copytree(srcDir, distDir)
        distDir = ''
        if not os.path.isabs(exportDirectory):
            distDir = self.directory + '/' + exportDirectory + '/btpy'
        else:
            distDir = exportDirectory + '/btpy'
        if not os.path.exists(distDir):
            os.mkdir(distDir)
        return self.root.export(distDir)
    
    #获取所有行为树，返回这些行为的路径的列表
    def getAllModelPaths(self):
        return self.root.getAllModelPaths([])
    
    def onWorkspaceRename(self, oldName, newName):
        self.name = newName
        self.root.name = newName
        self.root.onWorkspaceRename(oldName, newName)

'''
单例
'''
@utils.singleton
class WorkspaceMgr:
    def __init__(self):
        #<name, workspace>，工作区名 - 工作区
        self.workspaces = {}
        #当前复制的相关内容
        self.copyContent = {
            # 'copy_item': None, #当前复制的节点
        }
    
    def exist(self, name):
        return name in self.workspaces
    
    def remWorkspace(self, ws):
        return self.workspaces.pop(ws, None)
    
    def addWorkspace(self, ws):
        self.workspaces[ws.name] = ws
    
    def getWorkspace(self, name):
        return self.workspaces.get(name, None)
    
    def getModelByPath(self, path):
        if len(path) <= 0:
            return None
        ws = self.getWorkspace(path[0])
        modelItem = ws.getModelItemByPath(path[1:])
        return modelItem.model if modelItem else None

def _newWorkspace(name, directory, exportDirectory):
    if not utils.isValidName(name):
        return gg.ErrorCode.getErrorMsg(1, name=name)
    if not os.path.isdir(directory):
        return gg.ErrorCode.getErrorMsg(4, directory=directory)
    directory = directory.rstrip('\\').rstrip('/')
    filepath = directory + '/' + name + gg.WorkspaceFileSubfix
    if os.path.exists(filepath):
        return gg.ErrorCode.getErrorMsg(2, name=name)
    if WorkspaceMgr().exist(name):
        return gg.ErrorCode.getErrorMsg(2, name=name)
    try:
        workspace = Workspace(name, directory, exportDirectory)
        workspace.save()
        return workspace
    except PermissionError:
        return gg.ErrorCode.getErrorMsg(5, directory=directory)

def NewWorkspace(name, directory, exportDirectory):
    if utils.isPathHasKindFile(directory, gg.WorkspaceFileSubfix):
        return gg.ErrorCode.getErrorMsg(19)
    ret = _newWorkspace(name, directory, exportDirectory)
    if not isinstance(ret, Workspace):
        return ret
    workspace = ret
    WorkspaceMgr().addWorkspace(workspace)
    return None

def GetWorkspace(wsName):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if workspace is None:
        return {}
    return {
        'name': workspace.name,
        'directory': workspace.directory,
        'export_directory': workspace.exportDirectory,
    }

def WorkspaceNewDirectory(wsName, parentPath, directory):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(9, path=parentPath+[directory])+' 1'
    parentDir = workspace.getDirectoryItem(parentPath)
    dirItem = workspace.getDirectoryItem(parentPath+[directory])
    if not parentDir:
        return gg.ErrorCode.getErrorMsg(9, path=parentPath+[directory])+' 2'
    if dirItem:
        return gg.ErrorCode.getErrorMsg(9, path=parentPath+[directory])+' 3'
    dirItem = parentDir.addDirectory(directory)
    if not dirItem:
        return gg.ErrorCode.getErrorMsg(9, path=parentPath+[directory])+' 4'
    dirItem.save(workspace.getTreeRootDir() + gg.getPathFromList(parentPath) + '/')
    return None

def WorkspaceNewModel(wsName, parentPath, treeName):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    path = [wsName] + parentPath + [treeName]
    if not workspace:
        return gg.ErrorCode.getErrorMsg(10, path=path)+' 1'
    parentDir = workspace.getDirectoryItem(parentPath)
    model = workspace.getModelItem(parentPath, treeName)
    if not parentDir:
        return gg.ErrorCode.getErrorMsg(10, path=path)+' 2'
    if model:
        return gg.ErrorCode.getErrorMsg(10, path=path)+' 3'
    if not parentDir.newModel(path):
        return gg.ErrorCode.getErrorMsg(10, path=path)+' 4'
    return None

def EditWorkspace(oldData, newData):
    oldName = oldData['name']
    workspace = WorkspaceMgr().getWorkspace(oldName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(10, name=oldName)+' 1'
    newName = newData['name']
    if not utils.isValidName(newName):
        return gg.ErrorCode.getErrorMsg(1, name=newName)
    
    oldData = GetWorkspace(oldName)
    if oldData == newData:
        return gg.ErrorCode.getErrorMsg(60)
    
    if oldName != newName:
        filepath = workspace.directory + '/' + newName + gg.WorkspaceFileSubfix
        if os.path.exists(filepath):
            return gg.ErrorCode.getErrorMsg(2, name=newName)

        try:
            workspace.save()
            os.remove(workspace.getSaveFilePath())
        except Exception as e:
            # TODO 这里可以向view层发一个提示
            # return gg.ErrorCode.getErrorMsg(12, name=oldName) + '\n' + str(e)
            pass
        workspace.onWorkspaceRename(oldName, newName)
        WorkspaceMgr().remWorkspace(oldName)
        WorkspaceMgr().addWorkspace(workspace)
        try:
            oldTreeDir = filepath = workspace.directory + '/' + oldName
            newTreeDir = filepath = workspace.directory + '/' + newName
            os.rename(oldTreeDir, newTreeDir)
            workspace.saveWorkspaceFile()
            # workspace.save()
        except Exception as e:
            return gg.ErrorCode.getErrorMsg(22) + '\n' + str(e)
    workspace.exportDirectory = newData['export_directory']
    return None

def RemoveWorkspace(wsName):
    WorkspaceMgr().remWorkspace(wsName)
    return None

def SaveWorkspace(wsName):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)+' 1'
    try:
        workspace.save()
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(13, name=workspace.name) + '\n' + str(e)
    return None

def ImportModel(prePath, filepath):
    wsName = prePath[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)+' 1'
    dirItem = workspace.getDirectoryItem(prePath[1:])
    if not dirItem:
        return gg.ErrorCode.getErrorMsg(4, directory='/'.join(prePath))+' 2'
    _, tail = os.path.split(filepath)
    name = tail.split('.')[0]
    treeItem = workspace.getModelItem(prePath, name)
    key = gg.getKeyFromPath(prePath, name)
    if treeItem:
        return gg.ErrorCode.getErrorMsg(15, path=key)
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            data = json.load(f)
            model = mmodel.Model(key)
            if not model.load(data):
                return gg.ErrorCode.getErrorMsg(14, path=filepath)
            dirItem.addModel(prePath + [name], model)
    except Exception as e:
        logging.exception(e)
        return gg.ErrorCode.getErrorMsg(16, path=filepath)
    return None

def DeleteWorkspace(wsName):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return None
    try:
        workspace.deleteAllFiles()
        WorkspaceMgr().remWorkspace(wsName)
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(12, name=wsName) + '\n' + str(e)
    return None

def DeleteDirectory(path):
    wsName = path[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return None
    parentItem = workspace.getDirectoryItem(path[1:-1])
    dirItem = workspace.getDirectoryItem(path[1:])
    if not parentItem or not dirItem:
        return None
    try:
        dirPath = workspace.directory + '/' + workspace.name + '/' + gg.getKeyFromPath(path[1:])
        # os.rmdir(dirPath) #只能删除空目录
        shutil.rmtree(dirPath)
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(17, path=dirPath) + '\n' + str(e)
    parentItem.remDirectory(path[-1])
    return None

def DeleteTree(path):
    wsName = path[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)+' 1'
    parentItem = workspace.getDirectoryItem(path[1:-1])
    treeItem = workspace.getModelItemByPath(path[1:])
    if not parentItem or not treeItem:
        return None
    try:
        filePath = f'{workspace.directory}/{treeItem.model.id}' + gg.TreeFileSubfix
        if os.path.exists(filePath):
            os.remove(filePath)
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(18, path=filePath) + '\n' + str(e)
    parentItem.remModel(path[-1])
    workspace.saveWorkspaceFile()
    return None

def SaveAsWorkspace(wsName, newDirectory):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    if utils.isPathHasKindFile(newDirectory, gg.WorkspaceFileSubfix):
        return gg.ErrorCode.getErrorMsg(19)
    workspace.directory = newDirectory
    try:
        workspace.save()
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(13, name=workspace.name) + '\n' + str(e)
    return None

def OpenWorkspace(filepath):
    data = None
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(16, path=filepath) + str(e)
    
    wsName = data.get('name', '')
    #directory = data.get('directory', '')
    prePath, filename = os.path.split(filepath)
    directory = prePath
    #if not os.path.samefile(prePath, directory):
    #    return gg.ErrorCode.getErrorMsg(20, path=filepath) + ', 目录配置有问题'
    strs = filename.split('.')
    if wsName != strs[0]:
        return gg.ErrorCode.getErrorMsg(20, path=filepath) + ', 工作区名有问题'
    
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if workspace:
        return gg.ErrorCode.getErrorMsg(2, name=wsName)
    if utils.countPathHasKindFile(prePath, gg.WorkspaceFileSubfix) > 1:
        return gg.ErrorCode.getErrorMsg(21, path=prePath)
    
    workspace = Workspace(wsName, directory, data.get('export_dir', ''))
    try:
        workspace.load(data)
    except Exception as e:
        logging.exception(e)
        return str(e)
    WorkspaceMgr().addWorkspace(workspace)
    from controller.controller import Controller
    Controller.ViewWorkspaceOpened(wsName)
    return None
    
def GetWorkspaceViewData(wsName):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    return workspace.viewData()

def ExportWorkspace(wsName, exportDirectory):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    try:
        ret = workspace.export(exportDirectory)
        if ret:
            return gg.ErrorCode.getErrorMsg(22)
    except Exception as e:
        logging.exception(e)
        return gg.ErrorCode.getErrorMsg(22) + '\n' + str(e)
    return None
    
def ExportTree(path, exportDirectory):
    wsName = path[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    treeItem = workspace.getModelItemByPath(path[1:])
    if not treeItem:
        return gg.ErrorCode.getErrorMsg(23, path=gg.getPathFromList(path))
    try:
        ret = treeItem.export(exportDirectory)
        if ret:
            return gg.ErrorCode.getErrorMsg(24, path=gg.getPathFromList(path))
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(24, path=gg.getPathFromList(path)) + '\n' + str(e)
    return None
    
def GetAllModelPaths(wsName):
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    return workspace.getAllModelPaths()
    
def CheckModelError(path):
    wsName = path[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    treeItem = workspace.getModelItemByPath(path[1:])
    if not treeItem:
        return gg.ErrorCode.getErrorMsg(23, path=gg.getPathFromList(path))
    return treeItem.model.check()
    
def SaveTree(path):
    wsName = path[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    treeItem = workspace.getModelItemByPath(path[1:])
    if not treeItem:
        return gg.ErrorCode.getErrorMsg(23, path=gg.getPathFromList(path))
    try:
        prepath = workspace.directory + '/' + gg.getPathFromList(path[:-1]) + '/'
        treeItem.save(prepath)
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(25, path=gg.getPathFromList(path)) + '\n' + str(e)
    return None
    
def SaveAsTree(path, directory):
    wsName = path[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)
    treeItem = workspace.getModelItemByPath(path[1:])
    if not treeItem:
        return gg.ErrorCode.getErrorMsg(23, path=gg.getPathFromList(path))
    try:
        prepath = directory.rstrip('/\\') + '/'
        treeItem.save(prepath)
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(25, path=gg.getPathFromList(path)) + '\n' + str(e)
    return None

def CopyModelItem(path, id):
    model = WorkspaceMgr().getModelByPath(path)
    if not model:
        return gg.ErrorCode.getErrorMsg(23, path=gg.getPathFromList(path))
    item = model.getItem(id)
    if not item:
        return gg.ErrorCode.getErrorMsg(26, path=gg.getPathFromList(path), id=id)
    if CNT(item.itemType) in gg.ControlNodeTypeUncopyable:
        return None
    WorkspaceMgr().copyContent['copy_item'] = item.copy()
    return None

def PasteModelItem(path, id):
    pasteItem = WorkspaceMgr().copyContent.get('copy_item', None)
    if not pasteItem:
        return gg.ErrorCode.getErrorMsg(40)
    if pasteItem.id == id:
        return None
    model = WorkspaceMgr().getModelByPath(path)
    pasteItem = pasteItem.copy()
    model.CmdPasteItem(id, pasteItem)
    return None

def RenameDirectory(oldPath, newName):
    wsName = oldPath[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return None
    parentItem = workspace.getDirectoryItem(oldPath[1:-1])
    dirItem = workspace.getDirectoryItem(oldPath[1:])
    if not parentItem or not dirItem:
        return None
    try:
        oldDirPath = workspace.directory + '/' + gg.getKeyFromPath(oldPath)
        newDirPath = workspace.directory + '/' + gg.getKeyFromPath(oldPath[:-1]) + '/' + newName
        if os.path.exists(oldDirPath) and not os.path.exists(newDirPath):
            os.rename(oldDirPath, newDirPath)
        dirItem.name = newName
        dirItem.resetPath(oldPath[:-1])
        parentItem.remDirectory(oldPath[-1])
        parentItem.directory[dirItem.name] = dirItem
        workspace.save()
    except Exception as e:
        logging.exception(e)
        return gg.ErrorCode.getErrorMsg(27, path=gg.getPathFromList(oldPath), new_name=newName) + '\n' + str(e)
    return None

def RenameTree(oldPath, newName):
    wsName = oldPath[0]
    workspace = WorkspaceMgr().getWorkspace(wsName)
    if not workspace:
        return gg.ErrorCode.getErrorMsg(11, name=wsName)+' 1'
    parentItem = workspace.getDirectoryItem(oldPath[1:-1])
    treeItem = workspace.getModelItemByPath(oldPath[1:])
    if not parentItem or not treeItem:
        return None
    try:
        filePath = f'{workspace.directory}/{treeItem.model.id}' + gg.TreeFileSubfix
        treeItem.name = newName
        newPath = oldPath[:-1]
        newPath.append(newName)
        treeItem.model.id = gg.getKeyFromPath(newPath)
        newFilePath = f'{workspace.directory}/{treeItem.model.id}' + gg.TreeFileSubfix
        if os.path.exists(filePath):
            os.rename(filePath, newFilePath)
        parentItem.remModel(oldPath[-1])
        parentItem.trees[treeItem.name] = treeItem
        workspace.save()
    except Exception as e:
        return gg.ErrorCode.getErrorMsg(18, path=filePath) + '\n' + str(e)
    return None
