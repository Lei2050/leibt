from email import utils
import model.command.command as command
import model.items.factory as item_factory
import common.utils as utils

class CommandReplace(command.Command):
    def __init__(self, model, item, itemType):
        command.Command.__init__(self, model)
        
        self.oldItem = item
        self.itemType = itemType
        self.item = None
    
    def _check(self):
        if self.oldItem.hasChild():
            #如果被替换的节点有有效子节点，则不允许直接替换
            return False
        return True
    
    def redo(self):
        '''
        virtual method
        '''        
        child = self.item
        if not self.item:
            child = item_factory.Factory.New(utils.gen64Id(), self.model, self.itemType)
        parent = self.oldItem.parent
        idx = parent.findChildIdx(self.oldItem)
        parent.setChildByIdx(idx, child)
        if self.item != child:
            self.item = child

        return True

    def undo(self):
        '''
        virtual method
        '''
        parent = self.item.parent
        idx = parent.findChildIdx(self.item)
        parent.setChildByIdx(idx, self.oldItem)

        return True
        