import model.item_no_child as no_child
import g.gg as gg

class ItemCondition(no_child.ItemNoChild):
    def __init__(self, id, model, itemType):
        no_child.ItemNoChild.__init__(self, id, model, itemType)

    '''
    导出的合法性检测
    '''
    def checkExport(self):
        '''
        virtual method
        '''
        leftParam  = self.data.get('left_param', None)
        rightParam = self.data.get('right_param', None)
        if not leftParam:
            return self.errMsg(gg.ErrorCode.ConditionHasNoLeftParam)
        if not rightParam:
            return self.errMsg(gg.ErrorCode.ConditionHasNoRightParam)
        if not self.checkRightParamIllegal(leftParam):
            return self.errMsg(gg.ErrorCode.ConditionLeftParamIllegal)
        if not self.checkRightParamIllegal(rightParam):
            return self.errMsg(gg.ErrorCode.ConditionRightParamIllegal)
        return None
