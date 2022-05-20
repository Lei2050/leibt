import model.command.command as command
import model.items.factory as item_factory
import common.utils as utils
import g.gg as gg

CNT = gg.ControlNodeType

#在节点item，两个子节点交换位置
class CommandSwapSibling(command.Command):
    def __init__(self, model, item, idx1, idx2):
        command.Command.__init__(self, model)
        
        self.item = item
        self.idx1 = idx1
        self.idx2 = idx2
    
    def _check(self):
        if self.idx1 == self.idx2:
            return False
        if CNT(self.item.itemType) not in gg.ControlNodeTypeCombination:
            return False
        if CNT(self.item.itemType) == CNT.ConditionAction:
            if self.idx1 == 0 or self.idx2 == 0:
                return False
        item1 = self.item.getChildByIdx(self.idx1)
        item2 = self.item.getChildByIdx(self.idx2)
        if not item1 and not item2:
            return False
        return True
    
    def redo(self):
        '''
        virtual method
        '''
        return self.item.swapChild(self.idx1, self.idx2)

    def undo(self):
        '''
        virtual method
        '''
        return self.item.swapChild(self.idx1, self.idx2)
        