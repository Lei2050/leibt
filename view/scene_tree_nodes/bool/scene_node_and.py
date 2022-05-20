from view.scene_tree_nodes.scene_node import SceneNodeDrawFlag
import view.scene_tree_nodes.bool.scene_node_bool as scene_node_bool
import g.gg as gg
import controller.controller as controller

CNT = gg.ControlNodeType

class SceneNodeAnd(scene_node_bool.SceneNodeBool):
    def __init__(self, id, type):
        scene_node_bool.SceneNodeBool.__init__(self, id, type)

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        dit = gg.ControlNodeType(dropItemType)
        opSigns = []
        if dit in [CNT.Action, CNT.And, CNT.Or, CNT.Condition, CNT.FFalse, CNT.TTrue]:
            #添加为子节点
            opSigns.append(SceneNodeDrawFlag.OpSignRight)
            if not self.hasChild():
                opSigns.append(SceneNodeDrawFlag.OpSignCenterMiddle)
        if dit in [CNT.And, CNT.Or]:
            #允许前插
            opSigns.append(SceneNodeDrawFlag.OpSignLeft)
        if dit in (set(gg.ControlNodeTypeNonfixedChildBool) - set({CNT(self.type)})):
            opSigns.append(SceneNodeDrawFlag.OpSignCenterMiddle)
        ret = self.getOpSignsFocusedMap(opSigns)
        ret.update(self.canDropOpSignCommon(dropItemType))
        return ret
    
    def doDropOpSignCenterMiddle(self, dropItemType):
        '''
        virtual method
        '''
        selfType = CNT(self.type)
        dit = CNT(dropItemType)
        if self.hasChild() and dit in (set(gg.ControlNodeTypeNonfixedChildBool) - set({selfType})):
            #如果有子节点，可以替换为部分组合节点。比如随机序列替换为固定序列，子节点迁移到新的组合节点上
            controller.Controller.CmdReplaceNonfixedChildCombinationItem(self.modelPath, self.id, dropItemType)
        else:
            scene_node_bool.SceneNodeBool.doDropOpSignCenterMiddle(self, dropItemType)

    def doDropOpSignRight(self, itemType):
        '''
        virtual method
        '''
        controller.Controller.CmdAppendItem(self.modelPath, self.id, itemType)
    