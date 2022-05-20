from PyQt6.QtWidgets import QLineEdit

import view.scene_tree_nodes.scene_node as scene_node
import g.gg as gg

class SceneNodeFinish(scene_node.SceneNode):
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
    
    #保存属性面板上的参数，子类执行
    def onStoreDataFromPropertyWidget(self, widget, data):
        '''
        virtual method
        '''
        data['finish_status'] = self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditFinishStatus').text()

    #将控件属性数据显示在属性面板上，子类执行
    def onSetupPropertyWidgetData(self, widget, data):
        '''
        virtual method
        '''
        self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditFinishStatus').setText(data.get('finish_status', ''))
    