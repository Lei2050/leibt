from xml.etree.ElementPath import ops
from PyQt6.QtWidgets import QLineEdit

import view.scene_tree_nodes.scene_node as scene_node
import controller.controller as controller
import g.gg as gg

class SceneNodeAction(scene_node.SceneNode):
    def __init__(self, id, type):
        scene_node.SceneNode.__init__(self, id, type)
    
    def onPaint(self, painter, config):
        '''
        virtual method
        '''
        self.paintConnectedLine(painter)
        self.paintBackground(painter, config)   
        
        itemData = controller.Controller.GetModelItemData(self.modelPath, self.id)
        if itemData is None:
            return
        action = itemData.get('action', '')
        self.paintText(painter, action if action else self.getName(), config)
        self.paintCommentText(painter, config)

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        CNT = gg.ControlNodeType
        dit = gg.ControlNodeType(dropItemType)
        opSigns = []

        if dit in gg.ControlNodeTypeCombination:
            opSigns.append(scene_node.SceneNodeDrawFlag.OpSignLeft)

        if dit != self.type:
            if dit in gg.ControlNodeTypeActionsAndCombination and \
                (self.parent is None or (CNT(self.parent.type) not in gg.ControlNodeTypeBools and CNT(self.parent.type) != CNT.ConditionAction)):
                #如果父节点不是bool类型、也不是条件执行，则动作节点可以被动作类和组合类替换
                opSigns.append(scene_node.SceneNodeDrawFlag.OpSignCenterMiddle)
            if dit in gg.ControlNodeTypeBools and \
                ((CNT(self.parent.type) in [CNT.And, CNT.Or]) or (CNT(self.parent.type) in [CNT.ConditionAction] and self.parent.children[0] == self)):
                #如果父节点是组合bool类型、条件类型，则动作节点可以被bool类替换
                opSigns.append(scene_node.SceneNodeDrawFlag.OpSignCenterMiddle)
        ret = self.getOpSignsFocusedMap(opSigns)
        ret.update(self.canDropOpSignCommon(dropItemType))
        return ret
    
    #保存属性面板上的参数
    def onStoreDataFromPropertyWidget(self, widget, data):
        '''
        virtual method
        '''
        data['action'] = self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditAction').text()

    #将控件属性数据显示在属性面板上
    def onSetupPropertyWidgetData(self, widget, data):
        '''
        virtual method
        '''
        self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditAction').setText(data.get('action', ''))
