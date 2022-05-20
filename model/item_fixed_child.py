import model.item as iitem

#子节点数量固定的控件
class ItemFixedChild(iitem.Item):
    def __init__(self, id, model, itemType):
        iitem.Item.__init__(self, id, model, itemType)

    #移除子节点
    def removeChild(self, item):
        '''
        virtual method
        '''
        if not item:
            return False
        idx = self.findChildIdx(item)
        if -1 == idx:
            return False
        if self.children[idx]:
            self.children[idx].parent = None
            self.removeFromModel(self.model, self.children[idx])
        
        self.children[idx] = None
        
        return True
    
    def insertChildByIdx(self, idx, item):
        '''
        virtual method
        '''
        return False
