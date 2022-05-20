import g.gg as gg
import model.item_nonfixed_child as item_nonfixed_child

class ItemAnd(item_nonfixed_child.ItemNonfixedChild):
    def __init__(self, id, model, itemType):
        item_nonfixed_child.ItemNonfixedChild.__init__(self, id, model, itemType)
    
    '''
    导出的合法性检测
    '''
    def checkExport(self):
        '''
        virtual method
        '''
        if not self.hasChild():
            return self.errMsg(10201)
        return None
    
    def checkAddChild(self, idx, item):
        '''
        virtual method
        '''
        if not item:
            return False
        if item.itemType not in gg.ControlNodeTypeBools and item.itemType != gg.ControlNodeType.Action:
            return False
        return True
