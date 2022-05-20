import model.command.command as command
import model.items.factory as item_factory
import common.utils as utils
import g.gg as gg

CNT = gg.ControlNodeType

#在节点successorItem之前插入一个itemType类型的节点
class CommandInsert(command.Command):
    def __init__(self, model, successorItem, itemType):
        command.Command.__init__(self, model)
        
        #后继节点类型
        self.itemType = itemType
        #后继节点
        self.successorItem = successorItem
        #父节点
        self.parentItem = successorItem.parent
        #successorItem所在位置
        self.idx = self.parentItem.findChildIdx(self.successorItem)
        #增加的节点
        self.item = None
        #successorItem的直接父节点
        self.successorParentItem = None
    
    def redo(self):
        '''
        virtual method
        '''
        # item = self.model.addItemByIdAndType(self.parentItemId, self.itemType, self.successorItem.id if self.successorItem else 0)
        # child = iitem.Item(self.model, self.itemType) #插入的节点
        child  = self.item
        if not self.item:
            child = item_factory.Factory.New(utils.gen64Id(), self.model, self.itemType)
            if CNT(self.itemType) == CNT.ProbabilisticChoice:
                #如果是概率选择，则同时附加一个权重节点
                weight = item_factory.Factory.New(utils.gen64Id(), self.model, CNT.Weight)
                child.addChildItem(weight)
                self.successorParentItem = weight
            else:
                self.successorParentItem = child

        self.parentItem.setChildByIdx(self.idx, child)
        self.successorParentItem.addChildItem(self.successorItem)

        if self.item != child:
            self.item = child

        return True

    def undo(self):
        '''
        virtual method
        '''
        self.successorParentItem.removeChild(self.successorItem)
        self.parentItem.setChildByIdx(self.idx, self.successorItem)

        return True
        