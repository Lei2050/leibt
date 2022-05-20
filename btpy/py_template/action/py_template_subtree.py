import btpy.py_template.template_node as template_node
import btpy.py_template.bt as btpy
import btpy.py_template.const as btconst

class PyTemplateSubTree(template_node.TemplateNode):
    #传入的args是Argument类型的列表
    def __init__(self, id, subtree):
        template_node.TemplateNode.__init__(self, id)
        
        self.subtree = subtree
        self.subBT = None

    def updateImpl(self, bt, agent):
        if not self.subBT:
            module = None
            try:
                path = f"btpy.{self.subtree}"
                name = self.subtree
                module = __import__(path, fromlist=[name, ])
            except Exception as e:
                agent.errorMsg(str(e))
                return btconst.BT_FALSE
            
            self.subBT = btpy.BT(agent)
            module.Create(self.subBT)
        
        ret = self.subBT.exec()
        if ret in (btconst.BT_WAIT, btconst.BT_OVER):
            ret = btconst.BT_TRUE

        return ret
