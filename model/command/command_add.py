import model.command.command as command
import model.items.factory as item_factory
import common.utils as utils
import g.gg as gg

CNT = gg.ControlNodeType

#在节点parentItemId的第idx位置增加一个itemType类型的节点
#目前用于固定子节点增加子节点
class CommandAdd(command.Command):
    def __init__(self, model, parentItemId, itemType, idx = 0):
        command.Command.__init__(self, model)
        
        #父节点id
        self.parentItemId = parentItemId
        #后继节点类型
        self.itemType = itemType

        #父节点
        self.parentItem = self.model.getItem(self.parentItemId)
        #增加的节点
        self.item = None
        #新增节点的哪个位置
        self.addIdx = idx
    
    def redo(self):
        '''
        virtual method
        '''        
        child  = self.item
        if not self.item:
            child = item_factory.Factory.New(utils.gen64Id(), self.model, self.itemType)
            if CNT(self.parentItem.itemType) == CNT.ProbabilisticChoice:
                #如果是概率选择，则同时附加一个权重节点
                weight = item_factory.Factory.New(utils.gen64Id(), self.model, CNT.Weight)
                weight.setChildByIdx(0, child)
                child = weight

        # print(self.parentItemId, self.itemType, self.addIdx)

        self.parentItem.setChildByIdx(self.addIdx, child)

        if self.item != child:
            self.item = child
        
        return True

    def undo(self):
        '''
        virtual method
        '''
        self.parentItem.removeChild(self.item)
        
        return True
        