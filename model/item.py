import common.utils as utils
import model.items.factory as item_factory

class Item:
    def __init__(self, id, model, itemType):
        self.model = model
        self.id = id
        if not self.id:
            self.id = utils.gen64Id()
        self.itemType = itemType
        #字节点数量固定的控件，在子类的init中要直接确定children的值。
        #比如条件执行节点，他的子节点固定是3个，在init中：self.children = [None, None, None]
        self.children = []
        self.parent = None
        # self.model.addItem(self)

        self.data = {}

        self.init()
    
    def init(self):
        pass

    def dump(self, depth = 0):
        prefix = '    ' * depth
        print(prefix, self.id, self.itemType, self.data)
        for subNode in self.children:
            if subNode:
                subNode.dump(depth + 1)
    
    #复制，连同子节点
    def copy(self):
        newItem = item_factory.Factory.New(0, self.model, self.itemType)
        newItem.children = [None] * len(self.children)
        newItem.data = self.data.copy()
        for i, v in enumerate(self.children):
            if v:
                newChild = v.copy()
                newItem.children[i] = newChild
                newChild.parent = newItem
        return newItem
    
    def getData(self):
        # print('get', self.id, self.data)
        return self.data
    
    '''
    return - 是否有改变
    '''
    def updateData(self, data):
        oldData = self.data.copy()
        self.data.update(data)
        changed = oldData != self.data
        self.model.saved = not changed
        return changed
    
    def errMsg(self, errCode):
        return (self.id, errCode)
    
    def save(self):
        childrenData = []
        for child in self.children:
            childrenData.append(child.save() if child else None)
        saveData = {
            'id': self.id,
            'type': int(self.itemType),
            'data': self.data,
            'children': childrenData,
        }
        return saveData

    '''
    导出的合法性检测
    '''
    def checkExport(self):
        '''
        virtual method
        如果有错误，需要返回节点id和错误码，比如：return (self.id, gg.ErrorCode.ActionHasNoBehavior)
        '''
        return None
    
    def checkExports(self, collect):
        e = self.checkExport()
        if e is not None:
            collect.append(e)
        else:
            for subNode in self.children:
                if subNode:
                    subNode.checkExports(collect)
    
    '''
    检查一个行为是否合法
    '''
    def checkActionIllegal(self, action):
        return True
    
    '''
    检查左参数是否合法
    '''
    def checkLeftParamIllegal(self, param):
        return True
    
    '''
    检查右参数是否合法
    '''
    def checkRightParamIllegal(self, param):
        return True

    def addChildItem(self, item):
        pass
    
    def checkAddChild(self, idx, item):
        '''
        virtual method
        '''
        return True
    
    def getChildren(self):
        return self.children
    
    def clearChildren(self):
        self.children.clear()
    
    def hasChild(self):
        return len(list(filter(lambda x: x is not None, self.children))) > 0
    
    def removeFromModel(self, model, item):
        if not item:
            return
        if model:
            model.removeItem(item)
        if item.model == model:
            item.model = None
        for v in item.children:
            if v:
                v.removeFromModel(model, v)
    
    def addIntoModel(self, model, item):
        if not item:
            return
        if model:
            model.addItem(item)
        item.model = model
        for v in item.children:
            if v:
                v.addIntoModel(model, v)
    
    #查找item是否是子节点，找到了返回索引，否则返回-1
    def findChildIdx(self, item):
        if not item:
            return -1
        for i, v in enumerate(self.children):
            if item == v:
                return i
        return -1
    
    def getChildByIdx(self, idx):
        if idx < 0 or idx >= len(self.children):
            return None
        return self.children[idx]
    
    #这是第idx个子节点，item可以为None
    def setChildByIdx(self, idx, item):
        '''
        virtual method
        '''
        if item and not self.checkAddChild(idx, item):
            return False
        if idx < 0 or idx >= len(self.children):
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
    
    #移除子节点
    def removeChild(self, item):
        '''
        virtual method
        '''
        return False
    
    def insertChildByIdx(self, idx, item):
        if not item:
            return False
        self.children.insert(idx, item)
        item.parent = self
        self.addIntoModel(self.model, item)
        return True
    
    #交换两个子节点位置
    def swapChild(self, idx1, idx2):
        if idx1 < 0 or idx1 >= len(self.children):
            return False
        if idx2 < 0 or idx2 >= len(self.children):
            return False
        s1, s2 = self.children[idx1], self.children[idx2]
        self.children[idx1] = s2
        self.children[idx2] = s1
        return True
