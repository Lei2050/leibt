import model.item as iitem
import model.items.item_start as item_start
import model.items.bool.item_and as item_and
import model.items.bool.item_condition as item_condition
import model.items.bool.item_false as item_false
import model.items.bool.item_or as item_or
import model.items.bool.item_true as item_true
import model.items.action.item_action as item_action
import model.items.action.item_assignment as item_assignment
import model.items.action.item_calculate as item_calculate
import model.items.action.item_empty as item_empty
import model.items.action.item_finish as item_finish
import model.items.action.item_wait as item_wait
import model.items.action.item_subtree as item_subtree
import model.items.combination.item_condition_action as item_condition_action
import model.items.combination.item_exec_until_false as item_exec_until_false
import model.items.combination.item_exec_until_true as item_exec_until_true
import model.items.combination.item_order_list as item_order_list
import model.items.combination.item_probabilistic_choice as item_probabilistic_choice
import model.items.combination.item_random_choice as item_random_choice
import model.items.combination.item_random_list as item_random_list
import model.items.combination.item_weight as item_weight

import g.gg as gg

class Factory:
    Classes = {
        gg.ControlNodeType.Start               : item_start.ItemStart,
        gg.ControlNodeType.Or                  : item_or.ItemOr,
        gg.ControlNodeType.And                 : item_and.ItemAnd,
        gg.ControlNodeType.FFalse              : item_false.ItemFalse,
        gg.ControlNodeType.TTrue               : item_true.ItemTrue,
        gg.ControlNodeType.Condition           : item_condition.ItemCondition,
        gg.ControlNodeType.Wait                : item_wait.ItemWait,
        gg.ControlNodeType.Action              : item_action.ItemAction,
        gg.ControlNodeType.Assignment          : item_assignment.ItemAssignment,
        gg.ControlNodeType.Calculate           : item_calculate.ItemCalculate,
        gg.ControlNodeType.Finish              : item_finish.ItemFinish,
        gg.ControlNodeType.EmptyAction         : item_empty.ItemEmpty,
        gg.ControlNodeType.SubTree             : item_subtree.ItemSubTree,
        gg.ControlNodeType.ProbabilisticChoice : item_probabilistic_choice.ItemProbabilisticChoice,
        gg.ControlNodeType.RandomChoice        : item_random_choice.ItemRandomChoice,
        gg.ControlNodeType.OrderList           : item_order_list.ItemOrderList,
        gg.ControlNodeType.RandomList          : item_random_list.ItemRandomList,
        gg.ControlNodeType.ConditionAction     : item_condition_action.ItemConditionAction,
        gg.ControlNodeType.ExecUntilFalse      : item_exec_until_false.ItemExecUntilFalse,
        gg.ControlNodeType.ExecUnitlTrue       : item_exec_until_true.ItemExecUntilTrue,
        gg.ControlNodeType.Weight              : item_weight.ItemWeight,
    }

    @classmethod
    def New(cls, id, model, type):
        type = gg.ControlNodeType(type)
        c = cls.Classes.get(type, iitem.Item)
        return c(id, model, type)
