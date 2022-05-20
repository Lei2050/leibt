from email import utils
import model.command.command as command
import model.items.factory as item_factory
import common.utils as utils
import g.gg as gg

CNT = gg.ControlNodeType

#节点粘贴，item被pasteItem覆盖
class CommandPaste(command.Command):
    def __init__(self, model, item, pasteItem):
        command.Command.__init__(self, model)
        
        self.item = item
        self.pasteItem = pasteItem
        self.idx = self.item.parent.findChildIdx(self.item)
    
    def _check(self):
        if self.idx == -1:
            return False
        if not self.item or not self.pasteItem:
            return False
        if CNT(self.item.itemType) != CNT(self.pasteItem.itemType):
            #目前只支持同类型节点覆盖
            return False
        if CNT(self.item.itemType) in gg.ControlNodeTypeUncopyable:
            return False
        if CNT(self.pasteItem.itemType) in gg.ControlNodeTypeUncopyable:
            return False
        return True
    
    def redo(self):
        '''
        virtual method
        '''
        parent = self.item.parent
        parent.setChildByIdx(self.idx, self.pasteItem)

        return True

    def undo(self):
        '''
        virtual method
        '''
        parent = self.pasteItem.parent
        parent.setChildByIdx(self.idx, self.item)

        return True
        