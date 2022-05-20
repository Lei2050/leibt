import btpy.py_template.template_node as template_node
import btpy.py_template.const as btconst

class PyTemplateConditionAction(template_node.TemplateNode):
    #传入的args是Argument类型的列表
    def __init__(self, id):
        template_node.TemplateNode.__init__(self, id)
    
    def updateImpl(self, bt, agent):
        ret = self.children[0].updateImpl(bt, agent)
        if ret == btconst.BT_TRUE:
            self.execChildren = [self.children[1]]
        else:
            self.execChildren = [self.children[2]]
        return ret
