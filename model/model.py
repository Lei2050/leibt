import model.items.factory as item_factory
import model.command.history as cmd_history
import model.command.command_add as command_add
import model.command.command_insert_sibling as command_insert_sibling
import model.command.command_replace_ncci as command_replace_ncci
import model.command.command_replace as command_replace
import model.command.command_append as command_append
import model.command.command_delete as command_delete
import model.command.command_insert as command_insert
import model.command.command_swap_sibling as command_swap_sibling
import model.command.command_paste as command_paste
import model.exporter.factory as exporter_factory
import controller.controller as controller
import g.gg as gg
import common.utils as utils

CNT = gg.ControlNodeType

'''
行为树数据实体
'''
class Model:
    def __init__(self, k):
        self.id = k
        self.items = {}
        self.history = cmd_history.History()
        self.root = item_factory.Factory.New(utils.gen64Id(), self, gg.ControlNodeType.Start)
        self.saved = True

    def dump(self):
        print(self.items)
        self.root.dump()

    def getItem(self, itemId):
        return self.items.get(itemId, None)
            
    def addItem(self, item):
        if not item:
            return
        self.items[item.id] = item
    
    def removeItem(self, item):
        if not item:
            return
        self.items.pop(item.id, None)

    def getRoot(self):
        return self.root
    
    def redo(self):
        ret = self.history.redo()
        if ret:
            self.saved = False
        return ret

    def undo(self):
        ret = self.history.undo()
        if ret:
            self.saved = False
        return ret
    
    def check(self):
        errs = []
        self.root.checkExports(errs)
        return errs
    
    def exportFileName(self, exportDirectory):
        f = self.id.replace('/', '_')
        return f'{exportDirectory}/btpy/{f}.py'
    
    '''
    导出行为树
    成功返回 - true
    失败返回 - 错误列表
    '''
    def export(self, exportDirectory):
        errs = self.check()
        if errs:
            controller.Controller.ShowViewInfo(f'{self.id}导出失败，请执行错误检查！')
            return errs
        exporter = exporter_factory.Factory.New(self, exportDirectory, 'python')
        exporter.export()
        # controller.Controller.ClearViewInfo()
        controller.Controller.ShowViewInfo(f'{self.id}导出成功')
        return None

    def _execCmd(self, cmd):
        if cmd.Redo():
            self.saved = False
            self.history.addDoneCmd(cmd)
            path = gg.getPathFromStr(self.id)
            controller.Controller.ViewTreeChanged(path, False)
    
    #保存数据 - 返回可写入文本文件的数据
    def save(self):
        return self.root.save()
    
    def _load(self, data):
        item = item_factory.Factory.New(data['id'], self, CNT(data['type']))
        item.data = data['data']
        self.addItem(item)
        for i, sub in enumerate(data['children']):
            if sub is not None:
                subItem = self._load(sub)
                item.setChildByIdx(i, subItem)
        return item

    #从data中加载
    def load(self, data):
        self.removeItem(self.root)
        self.root = self._load(data)
        return True
    
    '''
    k - model的key
    pItemId - 父节点的id
    idx - 插入的位置
    itemType - 插入的节点类型
    successorItemId - 后继节点的id，如果该值>0，则是在pItemId和successorItemId之间插入
    '''
    def cmdAddItemByIdAndType(self, pItemId, itemType, idx):
        cmd = command_add.CommandAdd(self, pItemId, itemType, idx)
        self._execCmd(cmd)
    
    '''
    指定pItemId的节点追加一个子节点，主要是给子节点数量不固定的控件使用
    '''
    def cmdAppendItem(self, itemId, itemType):
        item = self.getItem(itemId)
        if not item:
            return
        cmd = command_append.CommandAppend(self, item, itemType)
        self._execCmd(cmd)
    
    '''
    在节点itemId前面插入类型为itemType的节点
    '''
    def CmdInsertItemBefore(self, itemId, itemType):
        item = self.getItem(itemId)
        if not item or not item.parent:
            return
        cmd = command_insert.CommandInsert(self, item, itemType)
        self._execCmd(cmd)

    '''
    #在当前选中节点之前插入一个节点（兄弟节点）
    '''
    def CmdInsertItemPreSibling(self, itemId, itemType):
        item = self.getItem(itemId)
        if not item or not item.parent:
            return
        parent = item.parent
        if CNT(parent.itemType) in (CNT.Weight, ):
            item = parent
            parent = parent.parent
        idx = item.parent.findChildIdx(item)
        cmd = command_insert_sibling.CommandInstertSibling(self, parent, itemType, idx)
        self._execCmd(cmd)

    '''
    #在当前选中节点之后插入一个节点（兄弟节点）
    '''
    def CmdInsertItemNextSibling(self, itemId, itemType):
        item = self.getItem(itemId)
        if not item or not item.parent:
            return
        parent = item.parent
        if CNT(parent.itemType) in (CNT.Weight, ):
            item = parent
            parent = parent.parent
        idx = item.parent.findChildIdx(item)
        cmd = command_insert_sibling.CommandInstertSibling(self, parent, itemType, idx+1)
        self._execCmd(cmd)
    
    '''
    #替换当前节点
    '''
    def CmdReplaceItem(self, itemId, itemType):
        item = self.getItem(itemId)
        if not item or not item.parent:
            return
        cmd = command_replace.CommandReplace(self, item, itemType)
        self._execCmd(cmd)
    
    '''
    #替换当前节点，并迁移子节点
    '''
    def CmdReplaceNonfixedChildCombinationItem(self, itemId, itemType):
        item = self.getItem(itemId)
        if not item:
            return
        cmd = command_replace_ncci.CmdReplaceNonfixedChildCombinationItem(self, item, itemType)
        self._execCmd(cmd)

    def CmdDelete(self, itemId):
        item = self.getItem(itemId)
        if not item:
            return
        cmd = command_delete.CommandDelete(self, item)
        self._execCmd(cmd)

    def CmdSwapSibling(self, itemId, upOrDown):
        item = self.getItem(itemId)
        if not item:
            return
        if CNT(item.itemType) == CNT.Weight:
            item = item.parent
        parent = item.parent
        if CNT(parent.itemType) not in gg.ControlNodeTypeCombination:
            return
        idx = parent.findChildIdx(item)
        idx2 = idx-1 if upOrDown else idx+1
        if idx2 < 0 or idx2 >= len(parent.getChildren()):
            return
        if CNT(parent.itemType) == CNT.ConditionAction:
            if idx == 0 or idx2 == 0:
                return False
        cmd = command_swap_sibling.CommandSwapSibling(self, parent, idx, idx2)
        self._execCmd(cmd)
    
    #粘贴节点，itemId将会被pasteItem覆盖
    def CmdPasteItem(self, itemId, pasteItem):
        item = self.getItem(itemId)
        if not item or not pasteItem:
            return
        cmd = command_paste.CommandPaste(self, item, pasteItem)
        self._execCmd(cmd)
