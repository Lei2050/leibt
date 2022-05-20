import random

import btpy.py_template.template_node as template_node
import btpy.py_template.const as btconst

class PyTemplateRandomList(template_node.TemplateNode):
    #传入的args是Argument类型的列表
    def __init__(self, id):
        template_node.TemplateNode.__init__(self, id)
    
    def updateImpl(self, bt, agent):
        self.execChildren = self.children.copy()
        random.shuffle(self.execChildren)
        return btconst.BT_TRUE
