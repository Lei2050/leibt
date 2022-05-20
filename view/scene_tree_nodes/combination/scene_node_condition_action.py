import math

from PyQt6.QtCore import QPoint, Qt, QRect
from PyQt6.QtGui import QFont, QColor, QPen, QBrush, QFontMetrics

import view.scene_tree_nodes.scene_node as scene_node
from view.dialog_scene_setting import DialogSceneSetting
import g.gg as gg
import view.utils as view_utils

class SceneNodeConditionAction(scene_node.SceneNode):
    def __init__(self, id, type):
        scene_node.SceneNode.__init__(self, id, type)
    
    #绘制背景
    def paintBackground(self, painter, config):
        sx, sy = self.position[0], self.position[1] - self.size[1]//2
        size = self.size
        color = DialogSceneSetting.GetColor('SceneNodePickedColor') if self.checkDrawFlag(scene_node.SceneNodeDrawFlag.Picked) else DialogSceneSetting.GetColor('SceneNodeBGColor')
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeLineColor'), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        brush = QBrush(color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)

        vertices = [(sx, sy + size[1] // 2), (sx + size[0] // 6, sy + size[1]), (sx + size[0] // 6 * 5, sy + size[1]),
            (sx + size[0], sy + size[1] // 6 * 5), (sx + size[0] // 6 * 5, sy + size[1] // 6 * 4),
            (sx + size[0], sy + size[1] // 2), (sx + size[0] // 6 * 5, sy + size[1] // 6 * 2), (sx + size[0], sy + size[1] // 6), 
            (sx + size[0] // 6 * 5, sy), (sx + size[0] // 6, sy)]
        view_utils.painterPolygon(painter, vertices, brush)
        if self.checkDrawFlag(scene_node.SceneNodeDrawFlag.Focused):
            brush = QBrush(DialogSceneSetting.GetColor('SceneNodeFocusColor'))
            view_utils.painterPolygon(painter, vertices, brush)
        view_utils.painterPolygonLine(painter, vertices)
    
    def onPaint(self, painter, config):
        '''
        virtual method
        '''
        sx, sy = self.position[0], self.position[1] - self.size[1]//2
        size = self.size
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeLineColor'), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for i, subNode in enumerate(self.children):
            if subNode:
                painter.drawLine(QPoint(sx + size[0], sy + size[1] // 6 + i * (size[1] // 3)), QPoint(subNode.position[0], subNode.position[1]))
        
        self.paintBackground(painter, config)
        self.paintText(painter, self.getName(), config)
        self.paintCommentText(painter, config)

        self._paintConditionTips(painter, config)
    
    #绘制条件、执行的文本提示
    def _paintConditionTips(self, painter, config):
        sx, sy = self.position[0], self.position[1] - self.size[1]//2
        size = self.size
        scale = config['scale']
        font = DialogSceneSetting.GetFont('SceneNodeFont')
        pointSize = math.ceil(font.pointSize() / 1.3 * scale)
        font.setPointSize(pointSize)
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeFontColor'), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setFont(font)

        infos = [
            #(center, text)
            ((sx + size[0], sy + size[1] // 6), '条件'),
            ((sx + size[0], sy + size[1] // 2), 'true'),
            ((sx + size[0], sy + size[1] // 6 * 5), 'false'),
        ]
        for v in infos:
            center, text = v[0], v[1]
            fontMetrics = QFontMetrics(font)
            boundingRect = fontMetrics.boundingRect(text)
            boundingRect = QRect(center[0] - boundingRect.width() // 2,
                center[1] - boundingRect.height() // 2,
                boundingRect.width(), boundingRect.height())
            painter.drawText(boundingRect.bottomLeft() - QPoint(0, pen.width()), text)

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
        
        if dit in gg.ControlNodeTypeActionsAndCombination:
            if self.children[1] is None:
                opSigns.append(scene_node.SceneNodeDrawFlag.OpSignRightMiddle)
            if self.children[2] is None:
                opSigns.append(scene_node.SceneNodeDrawFlag.OpSignRightBotton)
            if not self.hasChild():
                opSigns.append(scene_node.SceneNodeDrawFlag.OpSignCenterMiddle) #如果没有子节点就能替换
        if dit in gg.ControlNodeTypeBools or dit == gg.ControlNodeType.Action:
            #bool类型的节点和动作节点可以作为条件，动作节点的返回值作为参考
            if self.children[0] is None:
                opSigns.append(scene_node.SceneNodeDrawFlag.OpSignRightUp)
        ret = self.getOpSignsFocusedMap(opSigns)
        ret.update(self.canDropOpSignCommon(dropItemType))
        return ret
