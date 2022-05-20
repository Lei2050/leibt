import model.item_nonfixed_child as item_nonfixed_child
import g.gg as gg

CNT = gg.ControlNodeType

class ItemRandomList(item_nonfixed_child.ItemNonfixedChild):
    def __init__(self, id, model, itemType):
        item_nonfixed_child.ItemNonfixedChild.__init__(self, id, model, itemType)

    def checkAddChild(self, idx, item):
        '''
        virtual method
        '''
        if not item:
            return False
        if CNT(item.itemType) not in gg.ControlNodeTypeActionsAndCombination:
            return False
        return True
