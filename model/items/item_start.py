import model.item_fixed_child as item_fixed_child

class ItemStart(item_fixed_child.ItemFixedChild):
    def __init__(self, id, model, itemType):
        item_fixed_child.ItemFixedChild.__init__(self, id, model, itemType)
    
    def init(self):
        self.model.addItem(self)
        self.children = [None]
