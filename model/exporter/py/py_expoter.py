import model.exporter.exporter as exporter
import model.exporter.py.py_template as py_template

import g.gg as gg

CNT = gg.ControlNodeType

class PyExporter(exporter.Exporter):
    def __init__(self, model, exportDirectory):
        exporter.Exporter.__init__(self, model, exportDirectory)
        self.filename = self.model.exportFileName(exportDirectory)

        self.exportMethod = {
            CNT.Start               : self._exportStart,
            CNT.Or                  : self._exportOr,
            CNT.And                 : self._exportAnd,
            CNT.FFalse              : self._exportFFalse,
            CNT.TTrue               : self._exportTTrue,
            CNT.Condition           : self._exportCondition,
            CNT.Wait                : self._exportWait,
            CNT.Action              : self._exportAction,
            CNT.Assignment          : self._exportAssignment,
            CNT.Calculate           : self._exportCalculate,
            CNT.Finish              : self._exportFinish,
            CNT.EmptyAction         : self._exportEmptyAction,
            CNT.SubTree             : self._exportSubTree,
            CNT.ProbabilisticChoice : self._exportProbabilisticChoice,
            CNT.RandomChoice        : self._exportRandomChoice,
            CNT.OrderList           : self._exportOrderList,
            CNT.RandomList          : self._exportRandomList,
            CNT.ConditionAction     : self._exportConditionAction,
            CNT.ExecUntilFalse      : self._exportExecUntilFalse,
            CNT.ExecUnitlTrue       : self._exportExecUnitlTrue,
            CNT.Weight              : self._exportWeight,
        }
    
    def _exportStart(self, f, item):
        pass
    
    def _exportOr(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateOr({item.id})\n')
    
    def _exportAnd(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateAnd({item.id})\n')
    
    def _exportFFalse(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateFalse({item.id})\n')
    
    def _exportTTrue(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateTrue({item.id})\n')
    
    def _exportCondition(self, f, item):
        f.write( '    #=====================================================\n')
        leftParam = item.getData().get('left_param', '')
        operator = item.getData().get('operator', '')
        rightParam = item.getData().get('right_param', '')
        f.write(py_template.Condition.format(**{'tab':'    ', 'id':item.id, 'leftParam':leftParam, 'operator':operator, 'rightParam':rightParam}))
        f.write(f'    node_{item.id} = PyTemplateCondition_{item.id}({item.id})\n')
    
    def _exportWait(self, f, item):
        f.write( '    #=====================================================\n')
        waitTime = item.getData().get('wait_time', 0.0)
        f.write(f'    node_{item.id} = PyTemplateWait({item.id}, {waitTime})\n')

    def _exportAction(self, f, item):
        methodName, methoArgs = item.parse()
        args = []
        for v in methoArgs:
            if v[0] == 1:
                args.append(f'Argument(ArgumentType.TreeAttr, \'{v[1]}\')')
            elif v[0] == 2:
                args.append(f'Argument(ArgumentType.String, \'{v[1]}\')')
            elif v[0] == 3:
                args.append(f'Argument(ArgumentType.Int, {v[1]})')
            elif v[0] == 4:
                args.append(f'Argument(ArgumentType.Float, {v[1]})')
        
        f.write( '    #=====================================================\n')
        f.write( '    args = [' + ', '.join(args) + ']\n')
        f.write(f'    node_{item.id} = PyTemplateAction({item.id}, \'{methodName}\', *args)\n')
    
    def _exportAssignment(self, f, item):
        f.write( '    #=====================================================\n')
        leftParam, rightParam = item.getData().get('left_param', ''), item.getData().get('right_param', '')
        f.write(py_template.Assignment.format(**{'tab':'    ', 'id':item.id, 'leftParam':leftParam, 'action':rightParam}))
        f.write(f'    node_{item.id} = PyTemplateAssignment_{item.id}({item.id})\n')
    
    def _exportCalculate(self, f, item):
        f.write( '    #=====================================================\n')
        leftParam, rightParam = item.getData().get('left_param', ''), item.getData().get('right_param', '')
        f.write(py_template.Calculate.format(**{'tab':'    ', 'id':item.id, 'leftParam':leftParam, 'action':rightParam}))
        f.write(f'    node_{item.id} = PyTemplateCalculate_{item.id}({item.id})\n')
    
    def _exportFinish(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateFinish({item.id})\n')
    
    def _exportEmptyAction(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateEmpty({item.id})\n')
    
    def _exportSubTree(self, f, item):
        f.write( '    #=====================================================\n')
        subtree = item.getData().get('subtree', '')
        subtree = subtree.rstrip('/\\').replace('\\', '/').replace('/', '_')
        f.write(f'    node_{item.id} = PyTemplateSubTree({item.id}, \'{subtree}\')\n')
    
    def _exportProbabilisticChoice(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateProbabilisticChoice({item.id})\n')
    
    def _exportRandomChoice(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateRandomChoice({item.id})\n')
    
    def _exportOrderList(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateOrderList({item.id})\n')
    
    def _exportRandomList(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateRandomList({item.id})\n')
    
    def _exportConditionAction(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateConditionAction({item.id})\n')
    
    def _exportExecUntilFalse(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateExecUntilFalse({item.id})\n')
    
    def _exportExecUnitlTrue(self, f, item):
        f.write( '    #=====================================================\n')
        f.write(f'    node_{item.id} = PyTemplateExecUntilTrue({item.id})\n')
    
    def _exportWeight(self, f, item):
        pass
    
    def exportItem(self, f, item):
        if item.itemType == CNT.Weight:
            self.exportItem(f, item.children[0])
            return
        self.exportMethod.get(item.itemType)(f, item)
        for subItem in item.children:
            if subItem:
                self.exportItem(f, subItem)
                subItemId = subItem.id
                if subItem.itemType == CNT.Weight:
                    subItemId = subItem.children[0].id
                if item.itemType == CNT.ProbabilisticChoice:
                    weight = subItem.getData().get('weight', 1)
                    f.write(f'    node_{item.id}.addNode({weight}, node_{subItemId})\n')
                else:
                    f.write(f'    node_{item.id}.addNode(node_{subItemId})\n')

    def export(self):
        with open(self.filename, 'w', encoding='utf8') as f:
            f.write('from btpy.py_template.argument import *\n')
            f.write('from btpy.py_template.template_node import *\n')
            f.write('from btpy.py_template.action.py_template_action import *\n')
            f.write('from btpy.py_template.action.py_template_wait import *\n')
            f.write('from btpy.py_template.action.py_template_finish import *\n')
            f.write('from btpy.py_template.action.py_template_empty import *\n')
            f.write('from btpy.py_template.action.py_template_subtree import *\n')
            f.write('from btpy.py_template.bool.py_template_and import *\n')
            f.write('#from btpy.py_template.bool.py_template_condition import *\n')
            f.write('from btpy.py_template.bool.py_template_false import *\n')
            f.write('from btpy.py_template.bool.py_template_or import *\n')
            f.write('from btpy.py_template.bool.py_template_true import *\n')
            f.write('from btpy.py_template.combination.py_template_condition_action import *\n')
            f.write('from btpy.py_template.combination.py_template_exec_until_false import *\n')
            f.write('from btpy.py_template.combination.py_template_exec_until_true import *\n')
            f.write('from btpy.py_template.combination.py_template_order_list import *\n')
            f.write('from btpy.py_template.combination.py_template_probabilistic_choice import *\n')
            f.write('from btpy.py_template.combination.py_template_random_choice import *\n')
            f.write('from btpy.py_template.combination.py_template_random_list import *\n')
            f.write('import btpy.py_template.const as btconst\n')
            f.write('\n')
            f.write('def Create(bt):\n')
            if len(self.model.root.children) > 0:
                firstNode = self.model.root.children[0]
                if firstNode:
                    self.exportItem(f, firstNode)
                    f.write('    #=====================================================\n')
                    if firstNode:
                        f.write(f'    bt.root = node_{firstNode.id}\n')
            f.write('    pass')
