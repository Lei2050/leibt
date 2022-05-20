import model.command.command as command
import model.items.factory as item_factory
import common.utils as utils
import g.gg as gg

CNT = gg.ControlNodeType

#节点替换，子节点会按原位置放置到新的节点上。
#主要是用非固定子节点的组合节点使用
class CmdReplaceNonfixedChildCombinationItem(command.Command):
    def __init__(self, model, item, itemType):
        command.Command.__init__(self, model)
        
        self.oldItem = item
        self.itemType = itemType
        self.item = None
    
    def _check(self):
        if self.itemType == self.oldItem.itemType:
            return False
        return True

    def redo(self):
        '''
        virtual method
        '''
        child = self.item
        if not self.item:
            child = item_factory.Factory.New(utils.gen64Id(), self.model, self.itemType)
            if CNT(self.itemType) == CNT.ProbabilisticChoice:
                #新节点是概率选择节点，则需要额外插入权重节点
                for i, n in enumerate(self.oldItem.getChildren()):
                    weight = item_factory.Factory.New(utils.gen64Id(), self.model, CNT.Weight)
                    child.setChildByIdx(i, weight)
        
        parent = self.oldItem.parent
        idx = parent.findChildIdx(self.oldItem)
        parent.setChildByIdx(idx, child)

        if CNT(self.oldItem.itemType) == CNT.ProbabilisticChoice:
            #如果被替换节点是概率选择，保留权重节点，undo的时候比较方便，也能保留权重值
            for i, n in enumerate(self.oldItem.getChildren()):
                sn = n.children[0]
                n.setChildByIdx(0, None)
                child.setChildByIdx(i, sn)
        else:
            if CNT(self.itemType) == CNT.ProbabilisticChoice:
                for i, n in enumerate(self.oldItem.getChildren()):
                    child.children[i].setChildByIdx(0, n)
            else:
                for i, n in enumerate(self.oldItem.getChildren()):
                    child.setChildByIdx(i, n)
            self.oldItem.clearChildren()
        
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

        if CNT(self.item.itemType) == CNT.ProbabilisticChoice:
            #如果被替换节点是概率选择，保留权重节点，undo的时候比较方便，也能保留权重值
            for i, n in enumerate(self.item.getChildren()):
                sn = n.children[0]
                n.setChildByIdx(0, None)
                self.oldItem.setChildByIdx(i, sn)
        else:
            if CNT(self.oldItem.itemType) == CNT.ProbabilisticChoice:
                for i, n in enumerate(self.item.getChildren()):
                    self.oldItem.children[i].setChildByIdx(0, n)
            else:
                for i, n in enumerate(self.item.getChildren()):
                    self.oldItem.setChildByIdx(i, n)
            self.item.clearChildren()

        return True
        