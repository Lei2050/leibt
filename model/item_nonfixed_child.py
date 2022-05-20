import model.item as iitem

class ItemNonfixedChild(iitem.Item):
    def __init__(self, id, model, itemType):
        iitem.Item.__init__(self, id, model, itemType)

    def init(self):
        self.children = []

    def setChildByIdx(self, idx, item):
        '''
        virtual method
        '''
        if item and not self.checkAddChild(idx, item) or idx < 0:
            return False
        
        if idx >= len(self.children):
            self.addChildItem(item)
            return False
            
        if self.children[idx]:
            self.children[idx].parent = None
            self.removeFromModel(self.model, self.children[idx])
        
        self.children[idx] = item
        if item:
            item.parent = self
            #将item以及其子节点都加入model的map
            self.addIntoModel(self.model, item)
        return True

    def addChildItem(self, item):
        if not item:
            return False
        if not self.checkAddChild(len(self.children), item):
            return False
        self.children.append(item)
        item.parent = self
        self.addIntoModel(self.model, item)
        return True
    
    #移除子节点
    def removeChild(self, item):
        '''
        virtual method
        '''
        if not item:
            return False
        item.parent = None
        self.removeFromModel(self.model, item)
        self.children.remove(item)
        return True
    
    def insertChildByIdx(self, idx, item):
        if not item:
            return False
        self.children.insert(idx, item)
        item.parent = self
        self.addIntoModel(self.model, item)
        return True
