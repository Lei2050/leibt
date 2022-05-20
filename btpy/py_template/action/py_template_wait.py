import btpy.py_template.template_node as template_node
import btpy.py_template.const as btconst

class PyTemplateWait(template_node.TemplateNode):
    #interval - 毫秒数
    def __init__(self, id, interval):
        template_node.TemplateNode.__init__(self, id)
        
        self.waitTime = float(interval) // 1000.0

    def updateImpl(self, bt, agent):
        if self.waitTime <= 0:
            return btconst.BT_TRUE
        bt.waitFor(self.waitTime)
        return btconst.BT_WAIT
