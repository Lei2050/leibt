from view.scene_tree_nodes.scene_node import SceneNodeDrawFlag
import view.scene_tree_nodes.bool.scene_node_bool as scene_node_bool
import g.gg as gg

class SceneNodeTrue(scene_node_bool.SceneNodeBool):
    def __init__(self, id, type):
        scene_node_bool.SceneNodeBool.__init__(self, id, type)

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        CNT = gg.ControlNodeType
        dit = gg.ControlNodeType(dropItemType)
        ret = {}
        opSigns = []
        if dit != self.type and dit in [CNT.Action, CNT.And, CNT.Or, CNT.Condition, CNT.TTrue, CNT.FFalse]:
            opSigns.append(SceneNodeDrawFlag.OpSignCenterMiddle)
        if dit in [CNT.And, CNT.Or]:
            opSigns.append(SceneNodeDrawFlag.OpSignLeft)
        ret = self.getOpSignsFocusedMap(opSigns)
        ret.update(self.canDropOpSignCommon(dropItemType))
        return ret
    