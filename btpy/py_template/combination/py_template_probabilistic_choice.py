import random

import btpy.py_template.template_node as template_node
import btpy.py_template.const as btconst

class PyTemplateProbabilisticChoice(template_node.TemplateNode):
    #传入的args是Argument类型的列表
    def __init__(self, id):
        template_node.TemplateNode.__init__(self, id)
        
        self.weights = [] #[(weight, node)]
        self.weightSum = 0

    def addNode(self, weight, node):
        self.children.append(node)
        self.weights.append((int(weight), node))
        self.weightSum += int(weight)
    
    def _chooseNode(self):
        weightSum = int(self.weightSum)
        r = random.randint(1, weightSum)
        for w, n in self.weights:
            r -= w
            if r <= 0:
                return n
        return None
    
    def updateImpl(self, bt, agent):
        self.execChildren = [self._chooseNode()]
        return btconst.BT_TRUE
