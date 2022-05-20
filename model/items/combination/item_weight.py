import model.item_fixed_child as item_fixed_child
import g.gg as gg

CNT = gg.ControlNodeType

class ItemWeight(item_fixed_child.ItemFixedChild):
    def __init__(self, id, model, itemType):
        item_fixed_child.ItemFixedChild.__init__(self, id, model, itemType)
    
    def init(self):
        self.children = [None]

    def checkAddChild(self, idx, item):
        '''
        virtual method
        '''
        if not item:
            return False
        #没有子节点
        if idx != 0 or CNT(item.itemType) not in gg.ControlNodeTypeActionsAndCombination:
            return False
        return True
    
    def addChildItem(self, item):
        self.setChildByIdx(0, item)
        return item

    '''
    导出的合法性检测
    '''
    def checkExport(self):
        '''
        virtual method
        '''
        weight = self.getData().get('weight', 1)
        if weight < 1 or weight > 10000:
            return self.errMsg(gg.ErrorCode.WeightIllegalWeight)
        return None
    