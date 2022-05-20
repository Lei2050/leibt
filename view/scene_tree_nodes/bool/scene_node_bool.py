from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush

import view.scene_tree_nodes.scene_node as scene_node
import controller.controller as controller
from view.dialog_scene_setting import DialogSceneSetting
import g.gg as gg
import view.utils as view_utils

class SceneNodeBool(scene_node.SceneNode):
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
            (sx + size[0], sy + size[1] // 2), (sx + size[0] // 6 * 5, sy), (sx + size[0] // 6, sy)]
        view_utils.painterPolygon(painter, vertices, brush)
        if self.checkDrawFlag(scene_node.SceneNodeDrawFlag.Focused):
            brush = QBrush(DialogSceneSetting.GetColor('SceneNodeFocusColor'))
            view_utils.painterPolygon(painter, vertices, brush)
        view_utils.painterPolygonLine(painter, vertices)
