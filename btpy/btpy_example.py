from btpy.py_template.argument import *
from btpy.py_template.template_node import *
from btpy.py_template.action.py_template_action import *
from btpy.py_template.action.py_template_wait import *
from btpy.py_template.action.py_template_finish import *
from btpy.py_template.action.py_template_empty import *
from btpy.py_template.bool.py_template_and import *
#from btpy.py_template.bool.py_template_condition import *
from btpy.py_template.bool.py_template_false import *
from btpy.py_template.bool.py_template_or import *
from btpy.py_template.bool.py_template_true import *
from btpy.py_template.combination.py_template_condition_action import *
from btpy.py_template.combination.py_template_exec_until_false import *
from btpy.py_template.combination.py_template_exec_until_true import *
from btpy.py_template.combination.py_template_order_list import *
from btpy.py_template.combination.py_template_probabilistic_choice import *
from btpy.py_template.combination.py_template_random_choice import *
from btpy.py_template.combination.py_template_random_list import *
import btpy.py_template.const as btconst

def Create(bt):
    #=====================================================
    node_123459 = PyTemplateOrderList(123459)
    #=====================================================
    node_123460 = PyTemplateConditionAction(123460)
    #=====================================================

    class PyTemplateCondition_123467(TemplateNode):
        def __init__(self, id):
            TemplateNode.__init__(self, id)
        def updateImpl(self, bt, agent):
            val = getattr(bt, 'init', 0) != True
            return btconst.BT_TRUE if val else btconst.BT_FALSE
    node_123467 = PyTemplateCondition_123467(123467)
    node_123460.addNode(node_123467)
    #=====================================================
    node_123468 = PyTemplateOrderList(123468)
    #=====================================================
    node_123470 = PyTemplateWait(123470, 10000)
    node_123468.addNode(node_123470)
    #=====================================================

    class PyTemplateAssignment_123471(TemplateNode):
        def __init__(self, id):
            TemplateNode.__init__(self, id)
        def updateImpl(self, bt, agent):
            val = True
            setattr(bt, 'init', val)
            return btconst.BT_TRUE if val else btconst.BT_FALSE
    node_123471 = PyTemplateAssignment_123471(123471)
    node_123468.addNode(node_123471)
    node_123460.addNode(node_123468)
    #=====================================================
    node_123469 = PyTemplateEmpty(123469)
    node_123460.addNode(node_123469)
    node_123459.addNode(node_123460)
    #=====================================================

    class PyTemplateAssignment_123472(TemplateNode):
        def __init__(self, id):
            TemplateNode.__init__(self, id)
        def updateImpl(self, bt, agent):
            val = (0, 0, 0)
            setattr(bt, 'basePos', val)
            return btconst.BT_TRUE if val else btconst.BT_FALSE
    node_123472 = PyTemplateAssignment_123472(123472)
    node_123459.addNode(node_123472)
    #=====================================================
    node_123473 = PyTemplateRandomChoice(123473)
    #=====================================================
    args = [Argument(ArgumentType.Int, 101), Argument(ArgumentType.Int, 1201), Argument(ArgumentType.Int, 1), Argument(ArgumentType.Int, 10)]
    node_123463 = PyTemplateAction(123463, 'recvDamage', *args)
    node_123473.addNode(node_123463)
    #=====================================================
    node_123464 = PyTemplateWait(123464, 1000)
    node_123473.addNode(node_123464)
    #=====================================================
    node_123465 = PyTemplateOrderList(123465)
    #=====================================================
    args = [Argument(ArgumentType.TreeAttr, 'basePos')]
    node_123458 = PyTemplateAction(123458, 'randomWalk', *args)
    node_123465.addNode(node_123458)
    #=====================================================
    node_123466 = PyTemplateWait(123466, 5000)
    node_123465.addNode(node_123466)
    node_123473.addNode(node_123465)
    node_123459.addNode(node_123473)
    #=====================================================
    bt.root = node_123459
    pass