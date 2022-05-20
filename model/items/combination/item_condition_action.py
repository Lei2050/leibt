import g.gg as gg
import model.item_fixed_child as item_fixed_child

class ItemConditionAction(item_fixed_child.ItemFixedChild):
    def __init__(self, id, model, itemType):
        item_fixed_child.ItemFixedChild.__init__(self, id, model, itemType)
    
    def init(self):
        self.children = [None] * 3

    def checkAddChild(self, idx, item):
        '''
        virtual method
        '''
        if idx >= len(self.children):
            return False
        if idx == 0:
            #条件分支只接受bool类型的节点，和动作节点（其返回值将作为判断依据）
            if item.itemType not in gg.ControlNodeTypeBools and item.itemType != gg.ControlNodeType.Action:
                 return False
        else:
            if item.itemType not in gg.ControlNodeTypeActions and item.itemType not in gg.ControlNodeTypeCombination:
                return False
        return True

    def addChildItem(self, item):
        if self.children[1] is None:
            self.children[1] = item
        elif self.children[2] is None:
            self.children[2] = item
        else:
            return
        if item:
            item.parent = self
            #将item以及其子节点都加入model的map
            self.addIntoModel(self.model, item)

    '''
    导出的合法性检测
    '''
    def checkExport(self):
        '''
        virtual method
        '''
        if self.children[0] is None:
            return self.errMsg(gg.ErrorCode.ConditionActionHasNoCondition)
        elif self.children[1] is None:
            return self.errMsg(gg.ErrorCode.ConditionActionNoTrueBehavior)
        elif self.children[2] is None:
            return self.errMsg(gg.ErrorCode.ConditionActionNoFalseBehavior)
        return None
