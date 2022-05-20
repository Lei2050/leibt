Assignment = """
{tab}class PyTemplateAssignment_{id}(TemplateNode):
{tab}    def __init__(self, id):
{tab}        TemplateNode.__init__(self, id)
{tab}    def updateImpl(self, bt, agent):
{tab}        val = {action}
{tab}        setattr(bt, '{leftParam}', val)
{tab}        return btconst.BT_TRUE if val else btconst.BT_FALSE
"""

Calculate = """
{tab}class PyTemplateCalculate_{id}(TemplateNode):
{tab}    def __init__(self, id):
{tab}        TemplateNode.__init__(self, id)
{tab}    def updateImpl(self, bt, agent):
{tab}        val = {action}
{tab}        setattr(bt, '{leftParam}', val)
{tab}        return btconst.BT_TRUE if val else btconst.BT_FALSE
"""

Condition = """
{tab}class PyTemplateCondition_{id}(TemplateNode):
{tab}    def __init__(self, id):
{tab}        TemplateNode.__init__(self, id)
{tab}    def updateImpl(self, bt, agent):
{tab}        val = {leftParam} {operator} {rightParam}
{tab}        return btconst.BT_TRUE if val else btconst.BT_FALSE
"""
