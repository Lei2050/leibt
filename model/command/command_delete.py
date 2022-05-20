import model.command.command as command
import g.gg as gg

CNT = gg.ControlNodeType

class CommandDelete(command.Command):
    def __init__(self, model, item):
        command.Command.__init__(self, model)

        #父节点
        self.parentItem = item.parent
        #增加的节点
        self.item = item
        if self.parentItem.itemType == CNT.Weight:
            self.item = self.parentItem
            self.parentItem = self.item.parent
        #新增节点的哪个位置
        self.idx = self.parentItem.findChildIdx(self.item)
    
    def redo(self):
        '''
        virtual method
        '''
        self.parentItem.removeChild(self.item)

        return True

    def undo(self):
        '''
        virtual method
        '''
        CNT = gg.ControlNodeType
        parentItemType = CNT(self.parentItem.itemType)
        if parentItemType in (CNT.ExecUntilFalse, CNT.ExecUnitlTrue, CNT.OrderList, CNT.ProbabilisticChoice,
            CNT.RandomChoice, CNT.RandomList, CNT.And, CNT.Or): #这些都是子节点数量不固定的控件
            self.parentItem.insertChildByIdx(self.idx, self.item)
        elif parentItemType in (CNT.ConditionAction, CNT.Start): #这些都是子节点数量固定的控件
            self.parentItem.setChildByIdx(self.idx, self.item)
        else:
            return False

        return True
        