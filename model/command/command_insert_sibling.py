import model.command.command as command
import model.items.factory as item_factory
import common.utils as utils
import g.gg as gg

CNT = gg.ControlNodeType

#在节点parent的第idx位置插入一个itemType类型的节点
#目前用于非固定节点增加子节点。
class CommandInstertSibling(command.Command):
    def __init__(self, model, parent, itemType, idx = 0):
        command.Command.__init__(self, model)
        
        #父节点
        self.parent = parent
        #后继节点类型
        self.itemType = itemType
        #增加的节点
        self.item = None
        #插入的节点索引
        self.insertIdx = idx
    
    def redo(self):
        '''
        virtual method
        '''
        child  = self.item
        if not self.item:
            child = item_factory.Factory.New(utils.gen64Id(), self.model, self.itemType)
            if CNT(self.parent.itemType) == CNT.ProbabilisticChoice:
                #如果是概率选择，则同时附加一个权重节点
                weight = item_factory.Factory.New(utils.gen64Id(), self.model, CNT.Weight)
                weight.setChildByIdx(0, child)
                child = weight
        
        self.parent.insertChildByIdx(self.insertIdx, child)

        if self.item != child:
            self.item = child

        return True

    def undo(self):
        '''
        virtual method
        '''
        self.parent.removeChild(self.item)

        return True
        