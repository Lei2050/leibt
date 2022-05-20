import model.item_no_child as no_child

class ItemEmpty(no_child.ItemNoChild):
    def __init__(self, id, model, itemType):
        no_child.ItemNoChild.__init__(self, id, model, itemType)
