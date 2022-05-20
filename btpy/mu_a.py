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
    args = []
    node_1159719788313186796 = PyTemplateAction(1159719788313186796, 'f1', *args)
    #=====================================================
    bt.root = node_1159719788313186796
    pass