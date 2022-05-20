import model.item_no_child as no_child
import g.gg as gg

class ItemCalculate(no_child.ItemNoChild):
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
            return self.errMsg(gg.ErrorCode.CalculateHasNoLeftParam)
        if not rightParam:
            return self.errMsg(gg.ErrorCode.CalculateHasNoRightParam)
        if not self.checkLeftParamIllegal(leftParam):
            return self.errMsg(gg.ErrorCode.CalculateLeftParamIllegal)
        if not self.checkRightParamIllegal(rightParam):
            return self.errMsg(gg.ErrorCode.CalculateRightParamIllegal)
        return None
