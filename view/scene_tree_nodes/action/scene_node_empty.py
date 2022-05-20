import view.scene_tree_nodes.scene_node as scene_node
import g.gg as gg

class SceneNodeEmpty(scene_node.SceneNode):
    def __init__(self, id, type):
        scene_node.SceneNode.__init__(self, id, type)

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        ret = {}
        dit = gg.ControlNodeType(dropItemType)
        opSigns = []

        if dit in gg.ControlNodeTypeCombination:
            opSigns.append(scene_node.SceneNodeDrawFlag.OpSignLeft)

        if dit != self.type and (dit in gg.ControlNodeTypeActions or dit in gg.ControlNodeTypeCombination): #只能被这些节点替换
            opSigns.append(scene_node.SceneNodeDrawFlag.OpSignCenterMiddle)
        ret = self.getOpSignsFocusedMap(opSigns)
        ret.update(self.canDropOpSignCommon(dropItemType))
        return ret
    