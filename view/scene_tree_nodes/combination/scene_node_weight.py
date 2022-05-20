from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QPen, QBrush

import view.scene_tree_nodes.scene_node as scene_node
import controller.controller as controller
from view.dialog_scene_setting import DialogSceneSetting
import g.gg as gg

class SceneNodeWeight(scene_node.SceneNode):
    def __init__(self, id, type):
        scene_node.SceneNode.__init__(self, id, type)
        
    def onPaint(self, painter, config):
        '''
        virtual method
        '''
        self.paintConnectedLine(painter)
        
        size = self.size

        # painter.setBrush(DialogSceneSetting.GetColor('SceneNodePickedColor') if self.checkDrawFlag(scene_node.SceneNodeDrawFlag.Picked) else DialogSceneSetting.GetColor('SceneNodeBGColor'))
        
        color = DialogSceneSetting.GetColor('SceneNodePickedColor') if self.checkDrawFlag(scene_node.SceneNodeDrawFlag.Picked) else DialogSceneSetting.GetColor('SceneNodeBGColor')
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeLineColor'), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        brush = QBrush(color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)
        
        rect = QRect(self.position[0], self.position[1] - size[1]//2, size[0], size[1])
        painter.drawEllipse(rect)
        if self.checkDrawFlag(scene_node.SceneNodeDrawFlag.Focused):
            painter.setBrush(DialogSceneSetting.GetColor('SceneNodeFocusColor'))
            painter.drawEllipse(rect)
        
        itemData = controller.Controller.GetModelItemData(self.modelPath, self.id)
        if itemData is None:
            return
        weight  = itemData.get('weight', '')
        if not weight:
            weight = '1'
        self.paintText(painter, self.getName() + f'({weight})', config)
        
        self.paintCommentText(painter, config)

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        return {}
    
    #保存属性面板上的参数
    def onStoreDataFromPropertyWidget(self, widget, data):
        '''
        virtual method
        '''
        data['weight'] = self.findOneWidgetInWidget(widget, QSpinBox, 'spinBoxWeight').value()

    #将控件属性数据显示在属性面板上
    def onSetupPropertyWidgetData(self, widget, data):
        '''
        virtual method
        '''
        self.findOneWidgetInWidget(widget, QSpinBox, 'spinBoxWeight').setValue(data.get('weight', 1))
