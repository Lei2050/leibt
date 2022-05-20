from btpy.py_template.argument import *
from btpy.py_template.template_node import *
from btpy.py_template.action.py_template_action import *
from btpy.py_template.action.py_template_wait import *
from btpy.py_template.action.py_template_finish import *
from btpy.py_template.action.py_template_empty import *
from btpy.py_template.bool.py_template_and import *
from btpy.py_template.action.py_template_subtree import *
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
    node_14672487096885776876 = PyTemplateOrderList(14672487096885776876)
    #=====================================================
    args = [Argument(ArgumentType.String, 'before')]
    node_421758511809499628 = PyTemplateAction(421758511809499628, 'f2', *args)
    node_14672487096885776876.addNode(node_421758511809499628)
    #=====================================================
    node_14864118642028646892 = PyTemplateSubTree(14864118642028646892, 'mu_a')
    node_14672487096885776876.addNode(node_14864118642028646892)
    #=====================================================
    args = [Argument(ArgumentType.String, 'after')]
    node_554338916671885804 = PyTemplateAction(554338916671885804, 'f2', *args)
    node_14672487096885776876.addNode(node_554338916671885804)
    #=====================================================
    bt.root = node_14672487096885776876
    pass