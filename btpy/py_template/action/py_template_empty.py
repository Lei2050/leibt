import btpy.py_template.template_node as template_node
import btpy.py_template.const as btconst

class PyTemplateEmpty(template_node.TemplateNode):
    def __init__(self, id):
        template_node.TemplateNode.__init__(self, id)

    def updateImpl(self, bt, agent):
        return btconst.BT_TRUE
