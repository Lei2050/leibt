import btpy.py_template.template_node as template_node
import btpy.py_template.const as btconst

class PyTemplateAction(template_node.TemplateNode):
    #传入的args是Argument类型的列表
    def __init__(self, id, method, *args):
        template_node.TemplateNode.__init__(self, id)
        
        self.method = method
        self.args = args

    def updateImpl(self, bt, agent):
        ret = getattr(agent, self.method, None)(*[v.getValue(bt) for v in self.args])
        return btconst.BT_TRUE if ret else btconst.BT_FALSE
