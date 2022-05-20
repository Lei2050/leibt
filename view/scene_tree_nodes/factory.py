import view.scene_tree_nodes.scene_node as scene_node
import view.scene_tree_nodes.scene_node_start as scene_node_start
import view.scene_tree_nodes.bool.scene_node_or as scene_node_or
import view.scene_tree_nodes.bool.scene_node_and as scene_node_and
import view.scene_tree_nodes.bool.scene_node_false as scene_node_false
import view.scene_tree_nodes.bool.scene_node_true as scene_node_true
import view.scene_tree_nodes.bool.scene_node_condition as scene_node_condition
import view.scene_tree_nodes.action.scene_node_action as scene_node_action
import view.scene_tree_nodes.action.scene_node_assignment as scene_node_assignment
import view.scene_tree_nodes.action.scene_node_calculate as scene_node_calculate
import view.scene_tree_nodes.action.scene_node_empty as scene_node_empty
import view.scene_tree_nodes.action.scene_node_finish as scene_node_finish
import view.scene_tree_nodes.action.scene_node_subtree as scene_node_subtree
import view.scene_tree_nodes.action.scene_node_wait as scene_node_wait
import view.scene_tree_nodes.combination.scene_node_condition_action as scene_node_condition_action
import view.scene_tree_nodes.combination.scene_node_exec_until_false as scene_node_exec_until_false
import view.scene_tree_nodes.combination.scene_node_exec_until_true as scene_node_exec_until_true
import view.scene_tree_nodes.combination.scene_node_order_list as scene_node_order_list
import view.scene_tree_nodes.combination.scene_node_probabilistic_choice as scene_node_probabilistic_choice
import view.scene_tree_nodes.combination.scene_node_random_choice as scene_node_random_choice
import view.scene_tree_nodes.combination.scene_node_random_list as scene_node_random_list
import view.scene_tree_nodes.combination.scene_node_weight as scene_node_weight

import g.gg as gg

class Factory:
    Classes = {
        gg.ControlNodeType.Start               : scene_node_start.SceneNodeStart,
        gg.ControlNodeType.Or                  : scene_node_or.SceneNodeOr,
        gg.ControlNodeType.And                 : scene_node_and.SceneNodeAnd,
        gg.ControlNodeType.FFalse              : scene_node_false.SceneNodeFalse,
        gg.ControlNodeType.TTrue               : scene_node_true.SceneNodeTrue,
        gg.ControlNodeType.Condition           : scene_node_condition.SceneNodeCondition,
        gg.ControlNodeType.Wait                : scene_node_wait.SceneNodeWait,
        gg.ControlNodeType.Action              : scene_node_action.SceneNodeAction,
        gg.ControlNodeType.Assignment          : scene_node_assignment.SceneNodeAssignment,
        gg.ControlNodeType.Calculate           : scene_node_calculate.SceneNodeCalculate,
        gg.ControlNodeType.SubTree             : scene_node_subtree.SceneSubTree,
        gg.ControlNodeType.Finish              : scene_node_finish.SceneNodeFinish,
        gg.ControlNodeType.EmptyAction         : scene_node_empty.SceneNodeEmpty,
        gg.ControlNodeType.ProbabilisticChoice : scene_node_probabilistic_choice.SceneNodeProbabilisticChoice,
        gg.ControlNodeType.RandomChoice        : scene_node_random_choice.SceneNodeRandomChoice,
        gg.ControlNodeType.OrderList           : scene_node_order_list.SceneNodeOrderList,
        gg.ControlNodeType.RandomList          : scene_node_random_list.SceneNodeRandomList,
        gg.ControlNodeType.ConditionAction     : scene_node_condition_action.SceneNodeConditionAction,
        gg.ControlNodeType.ExecUntilFalse      : scene_node_exec_until_false.SceneNodeExecUntilFalse,
        gg.ControlNodeType.ExecUnitlTrue       : scene_node_exec_until_true.SceneNodeExecUntilTrue,
        gg.ControlNodeType.Weight              : scene_node_weight.SceneNodeWeight,
    }

    @classmethod
    def New(cls, id, type):
        Node = cls.Classes.get(type, None)
        if not Node:
            return scene_node.SceneNode
        return Node(id, type)
