import model.item_no_child as no_child
import g.gg as gg

class ItemAssignment(no_child.ItemNoChild):
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
            return self.errMsg(gg.ErrorCode.AssignmentHasNoLeftParam)
        if not rightParam:
            return self.errMsg(gg.ErrorCode.AssignmentHasNoRightParam)
        if not self.checkLeftParamIllegal(leftParam):
            return self.errMsg(gg.ErrorCode.AssignmentLeftParamIllegal)
        if not self.checkRightParamIllegal(rightParam):
            return self.errMsg(gg.ErrorCode.AssignmentRightParamIllegal)
        return None
