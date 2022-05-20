import btpy.py_template.const as btconst

class TemplateNode:
    def __init__(self, id):
        self.id = id
        #原生节点
        self.children = []
        #当前需要被执行的节点。
        #比如随机选择节点，原生有3个节点，len(self.children) == 3，
        # 节点执行随机挑选一个作为执行节点加入self.execChildren，len(self.execChildren) == 1
        self.execChildren = []
    
    def addNode(self, node):
        self.children.append(node)

    def updateImpl(self, bt, agent):
        return btconst.BT_TRUE
