import model.item_no_child as no_child

class ItemSubTree(no_child.ItemNoChild):
    def __init__(self, id, model, itemType):
        no_child.ItemNoChild.__init__(self, id, model, itemType)

    '''
    导出的合法性检测
    '''
    def checkExport(self):
        '''
        virtual method
        '''
        subtree  = self.data.get('subtree', '')
        if not subtree:
            return self.errMsg(20702)
        path = subtree.rstrip('/\\').replace('\\', '/')
        if path == self.model.id:
            return self.errMsg(20703)
        path = path.split('/')
        from model.workspace import WorkspaceMgr
        model = WorkspaceMgr().getModelByPath(path)
        if not model:
            return self.errMsg(20701)
        return None
