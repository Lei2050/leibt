import model.item_no_child as no_child
import g.gg as gg
import view.gg as view_gg

class ItemAction(no_child.ItemNoChild):
    def __init__(self, id, model, itemType):
        no_child.ItemNoChild.__init__(self, id, model, itemType)
    
    def parse(self):
        action = self.data.get('action', None)
        leftBracketIdx = action.find('(')
        if leftBracketIdx == -1:
            return False
        rightBracketIdx = action.find(')')
        if rightBracketIdx == -1:
            return False
        methodName = action[:leftBracketIdx]

        ss = action[leftBracketIdx+1:rightBracketIdx]
        args = []
        if ss:
            for s in ss.split(','):
                s = s.strip()
                try:
                    val = eval(s)
                    if isinstance(val, str):
                        args.append((2, val))
                    elif isinstance(val, int):
                        args.append((3, val))
                    elif isinstance(val, float):
                        args.append((4, val))
                    else:
                        view_gg.InfoPlainTextEditAppenText(f'行动节点ID：{str(self.id)}, ‘{s}’参数解析失败')
                        return False
                except Exception as e:
                    if action.find('\'') != -1:
                        view_gg.InfoPlainTextEditAppenText(f'行动节点ID：{str(self.id)}, ‘{s}’参数解析失败')
                        return False
                    args.append((1, s.strip('\'')))
        return (methodName, args)
    
    '''
    导出的合法性检测
    '''
    def checkExport(self):
        '''
        virtual method
        '''
        action = self.data.get('action', None)
        if not action:
            return self.errMsg(gg.ErrorCode.ActionHasNoBehavior)
        ret = self.parse()
        if ret == False:
            return self.errMsg(gg.ErrorCode.ActionBehaviorIllegal)
        return None
    