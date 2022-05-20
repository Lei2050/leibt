from PyQt6.QtWidgets import QLineEdit

import view.scene_tree_nodes.scene_node as scene_node
import controller.controller as controller
import g.gg as gg

CNT = gg.ControlNodeType

class SceneNodeProbabilisticChoice(scene_node.SceneNode):
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
        random = itemData.get('random', '')
        self.paintText(painter, self.getName() + f'({random})', config)
        self.paintCommentText(painter, config)

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        dit = CNT(dropItemType)
        ret = {}
        opSigns = []
        # if dit == CNT(self.type):
        #     ret = {}

        if dit in gg.ControlNodeTypeCombination:
            opSigns.append(scene_node.SceneNodeDrawFlag.OpSignLeft)
        
        if dit in gg.ControlNodeTypeActionsAndCombination:
            opSigns.append(scene_node.SceneNodeDrawFlag.OpSignRight)
            if not self.hasChild():
                opSigns.append(scene_node.SceneNodeDrawFlag.OpSignCenterMiddle) #如果没有子节点就能替换
        if dit in (set(gg.ControlNodeTypeNonfixedChildCombination) - set({CNT(self.type)})):
            opSigns.append(scene_node.SceneNodeDrawFlag.OpSignCenterMiddle)
        ret = self.getOpSignsFocusedMap(opSigns)
        ret.update(self.canDropOpSignCommon(dropItemType))
        return ret
    
    def doDropOpSignCenterMiddle(self, dropItemType):
        '''
        virtual method
        '''
        selfType = CNT(self.type)
        dit = CNT(dropItemType)
        if self.hasChild() and dit in (set(gg.ControlNodeTypeNonfixedChildCombination) - set({selfType})):
            #如果有子节点，可以替换为部分组合节点。比如随机序列替换为固定序列，子节点迁移到新的组合节点上
            controller.Controller.CmdReplaceNonfixedChildCombinationItem(self.modelPath, self.id, dropItemType)
        else:
            scene_node.SceneNode.doDropOpSignCenterMiddle(self, dropItemType)
    
    def doDropOpSignRight(self, itemType):
        '''
        virtual method
        '''
        controller.Controller.CmdAppendItem(self.modelPath, self.id, itemType)
    
    #保存属性面板上的参数，子类执行
    def onStoreDataFromPropertyWidget(self, widget, data):
        '''
        virtual method
        '''
        data['random'] = self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditRandom').text()

    #将控件属性数据显示在属性面板上，子类执行
    def onSetupPropertyWidgetData(self, widget, data):
        '''
        virtual method
        '''
        self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditRandom').setText(data.get('random', ''))
    