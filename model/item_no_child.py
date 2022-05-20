import model.item as iitem

#子节点数量固定的控件
class ItemNoChild(iitem.Item):
    def __init__(self, id, model, itemType):
        iitem.Item.__init__(self, id, model, itemType)
    
    def init(self):
        self.children = []
    
    def checkAddChild(self, idx, item):
        '''
        virtual method
        '''
        #没有子节点
        return False

    def setChildByIdx(self, idx, item):
        '''
        virtual method
        '''
        #没有子节点
        return False

    def insertChildByIdx(self, idx, item):
        '''
        virtual method
        '''
        #没有子节点
        return False
    
