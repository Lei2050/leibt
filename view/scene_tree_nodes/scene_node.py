import enum
import math

from PyQt6.QtGui import QColor, QFont, QPen, QBrush, QFontMetrics
from PyQt6.QtCore import QRect, QPoint, Qt
from PyQt6.QtWidgets import QLineEdit, QComboBox

import g.gg as gg
import view.gg as view_gg
import common.utils as utils
import view.utils as view_utils
from view.dialog_scene_setting import DialogSceneSetting
from controller.controller import Controller
from g.config import Config

import data.item as data_item

class SceneNodeDrawFlag(enum.IntFlag):
    Picked             = enum.auto()
    Focused            = enum.auto()
    Error              = enum.auto()
    OpSignLeft         = enum.auto() #操作指示符 - 左边箭头
    OpSignCenterUp     = enum.auto() #操作指示符 - 中间向上箭头
    OpSignCenterMiddle = enum.auto() #操作指示符 - 中间方块
    OpSignCenterBotton = enum.auto() #操作指示符 - 中间向下箭头
    OpSignRightUp      = enum.auto() #操作指示符 - 右边第一个箭头
    OpSignRightMiddle  = enum.auto() #操作指示符 - 右边第二个箭头
    OpSignRightBotton  = enum.auto() #操作指示符 - 右边第三个箭头
    OpSignRight        = enum.auto() #操作指示符 - 右边箭头
    OpSignFocusedLeft         = enum.auto() #操作指示符 - 左边箭头
    OpSignFocusedCenterUp     = enum.auto() #操作指示符 - 中间向上箭头
    OpSignFocusedCenterMiddle = enum.auto() #操作指示符 - 中间方块
    OpSignFocusedCenterBotton = enum.auto() #操作指示符 - 中间向下箭头
    OpSignFocusedRightUp      = enum.auto() #操作指示符 - 右边第一个箭头
    OpSignFocusedRightMiddle  = enum.auto() #操作指示符 - 右边第二个箭头
    OpSignFocusedRightBotton  = enum.auto() #操作指示符 - 右边第三个箭头
    OpSignFocusedRight        = enum.auto() #操作指示符 - 右边箭头
    OpSignAll = OpSignLeft | OpSignCenterUp | OpSignCenterMiddle | OpSignCenterBotton | OpSignRightUp | OpSignRightMiddle | OpSignRightBotton | OpSignRight
    OpSignFocusedAll = OpSignFocusedLeft | OpSignFocusedCenterUp | OpSignFocusedCenterMiddle | OpSignFocusedCenterBotton | \
                        OpSignFocusedRightUp | OpSignFocusedRightMiddle | OpSignFocusedRightBotton | OpSignFocusedRight

OpSignFocusedMap = {
    SceneNodeDrawFlag.OpSignLeft         : SceneNodeDrawFlag.OpSignFocusedLeft, 
    SceneNodeDrawFlag.OpSignCenterUp     : SceneNodeDrawFlag.OpSignFocusedCenterUp, 
    SceneNodeDrawFlag.OpSignCenterMiddle : SceneNodeDrawFlag.OpSignFocusedCenterMiddle,
    SceneNodeDrawFlag.OpSignCenterBotton : SceneNodeDrawFlag.OpSignFocusedCenterBotton, 
    SceneNodeDrawFlag.OpSignRightUp      : SceneNodeDrawFlag.OpSignFocusedRightUp, 
    SceneNodeDrawFlag.OpSignRightMiddle  : SceneNodeDrawFlag.OpSignFocusedRightMiddle,
    SceneNodeDrawFlag.OpSignRightBotton  : SceneNodeDrawFlag.OpSignFocusedRightBotton, 
    SceneNodeDrawFlag.OpSignRight        : SceneNodeDrawFlag.OpSignFocusedRight,
}

class SceneNode:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.children = []
        self.parent = None

        self.span     = [0, 0]
        self.position = [0, 0]
        self.size     = [0, 0]

        self.drawFlag = 0
        
        self.modelPath = None
    
    def childNum(self):
        return len(list(filter(lambda x: x is not None, self.children)))
    
    #是否有子节点
    def hasChild(self):
        return self.childNum() > 0
    
    def setDrawFlag(self, v):
        self.drawFlag |= v
    
    def unsetDrawFlag(self, v):
        self.drawFlag &= ~v
    
    def checkDrawFlag(self, v):
        return (self.drawFlag & v) > 0
    
    def unfocused(self):
        self.unsetDrawFlag(SceneNodeDrawFlag.OpSignAll | SceneNodeDrawFlag.OpSignFocusedAll | SceneNodeDrawFlag.Focused)
    
    def getWorkspaceName(self):
        return self.modelPath[0]

    def getModel(self):
        Controller.GetModel(self.modelPath)
    
    def getModelItem(self):
        return self.getModel().getItem(self.id)

    def calRectSize(self, defaultSize):
        '''
        virtual method
        '''
        #TODO 这里想自定义各种控件的大小，大小不一的控件，在计算位置时会有点小麻烦
        self.size = list(defaultSize)
    
    def dump(self, depth):
        prefix = '    ' * depth
        print(prefix, self.id, self.type, self.position, self.span)
        for subNode in self.children:
            if subNode:
                subNode.dump(depth + 1)
    
    def getName(self):
        d = data_item.Data.get(int(self.type), None)
        if d:
            return d.get('show_name', '未知')
        return '未知'
    
    #允许snode为空，主要是为了判断有些节点的有些子节点位置是否有控件
    def addChild(self, snode):
        self.children.append(snode)
    
    #计算一个节点所占的空间大小，该空间大小包括所有自节点
    def calSize(self, config):
        nodeSize = config.get('node_size', gg.ControlNodeDefaultSize)
        self.calRectSize(nodeSize)
        margin = config.get('margin', gg.ControlNodeMargin)
        subH, subW = 0, 0
        for subNode in self.children:
            if subNode:
                subNode.calSize(config)
                subH += subNode.span[1]
                if subW < subNode.span[0]:
                    subW = subNode.span[0]
        childNum = self.childNum()
        if childNum > 0:
            subH += int((childNum - 1) * margin[1])
        subW += int(self.size[0] + (margin[0] if subW > 0 else 0))
        self.span[0] = int(subW)
        self.span[1] = int(subH if subH > self.size[1] else self.size[1])
    
    #计算每个节点的起始位置
    def calLocation(self, offset, config):
        margin = config.get('margin', gg.ControlNodeMargin)
        self.position[0] = int(offset[0])
        self.position[1] = int(offset[1] + self.span[1]//2)
        h = 0
        for subNode in self.children:
            if subNode:
                subOffset = (offset[0] + self.size[0] + margin[0], offset[1] + h)
                subNode.calLocation(subOffset, config)
                h += subNode.span[1] + margin[1]
    
    def paintOpSign(self, painter, opSign, focused):
        sx, sy = self.position[0], self.position[1] - self.size[1]//2
        size = self.size
        vertices = []
        if SceneNodeDrawFlag.OpSignLeft == opSign:
            vertices = [(sx, sy + size[1] // 2), (sx + size[0] // 6, sy + size[1]), (sx + size[0] // 6, sy)]
        elif SceneNodeDrawFlag.OpSignCenterUp == opSign:
            vertices = [(sx + size[0] // 2, sy), (sx + size[0] // 3, sy + size[1] // 5), (sx + size[0] // 3 * 2, sy + size[1] // 5)]
        elif SceneNodeDrawFlag.OpSignCenterMiddle == opSign:
            vertices = [(sx + size[0] // 3, sy + size[1] // 5 * 2), (sx + size[0] // 3, sy + size[1] // 5 * 3),
                (sx + size[0] // 3 * 2, sy + size[1] // 5 * 3), (sx + size[0] // 3 * 2, sy + size[1] // 5 * 2)]
        elif SceneNodeDrawFlag.OpSignCenterBotton == opSign:
            vertices = [(sx + size[0] // 2, sy + size[1]), (sx + size[0] // 3 * 2, sy + size[1] // 5 * 4), (sx + size[0] // 3, sy + size[1] // 5 * 4)]
        elif SceneNodeDrawFlag.OpSignRightUp == opSign:
            vertices = [(sx + self.size[0] // 6 * 5, sy), (sx + size[0] // 6 * 5, sy + size[1] // 3), (sx + size[0], sy + size[1] // 6)]
        elif SceneNodeDrawFlag.OpSignRightMiddle == opSign:
            vertices = [(sx + self.size[0] // 6 * 5, sy + size[1] // 3), (sx + size[0] // 6 * 5, sy + size[1] // 3 * 2), (sx + size[0], sy + size[1] // 2)]
        elif SceneNodeDrawFlag.OpSignRightBotton == opSign:
            vertices = [(sx + self.size[0] // 6 * 5, sy + size[1] // 3 * 2), (sx + size[0] // 6 * 5, sy + size[1]), (sx + size[0], sy + size[1] // 6 * 5)]
        elif SceneNodeDrawFlag.OpSignRight == opSign:
            vertices = [(sx + size[0] // 6 * 5, sy), (sx + size[0] // 6 * 5, sy + size[1]), (sx + size[0], sy + size[1] // 2)]
        brush = QBrush(DialogSceneSetting.GetColor('SceneNodeOpSignFocusColor') if focused else DialogSceneSetting.GetColor('SceneNodeOpSignColor'))
        view_utils.painterPolygon(painter, vertices, brush)
    
    def paintOpSigns(self, painter):
        for s1, s2 in OpSignFocusedMap.items():
            cs1, cs2 = self.checkDrawFlag(s1), self.checkDrawFlag(s2)
            if cs1 or cs2:
                self.paintOpSign(painter, s1, cs2)

    #绘制与子结点的链接
    def paintConnectedLine(self, painter):
        size = self.size
        # painter.setBrush(DialogSceneSetting.GetColor('SceneNodeLineColor'))
        # pen = QPen(DialogSceneSetting.GetColor('SceneNodeLineColor'), 3, Qt.PenStyle.DashDotLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeLineColor'), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for subNode in self.children:
            if subNode:
                painter.drawLine(QPoint(self.position[0] + size[0], self.position[1]), QPoint(subNode.position[0], subNode.position[1]))
    
    #绘制背景
    def paintBackground(self, painter, config):
        size = self.size
        retRound = config.get('rect_round', gg.ControlNodeRectRound)
        color = DialogSceneSetting.GetColor('SceneNodePickedColor') if self.checkDrawFlag(SceneNodeDrawFlag.Picked) else DialogSceneSetting.GetColor('SceneNodeBGColor')
        # painter.setBrush(DialogSceneSetting.GetColor('SceneNodePickedColor') if self.checkDrawFlag(SceneNodeDrawFlag.Picked) else DialogSceneSetting.GetColor('SceneNodeBGColor'))
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeLineColor'), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        brush = QBrush(color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)

        rect = QRect(self.position[0], self.position[1] - size[1]//2, size[0], size[1])
        painter.drawRoundedRect(rect, retRound[0], retRound[1])
        if self.checkDrawFlag(SceneNodeDrawFlag.Focused):
            painter.setBrush(DialogSceneSetting.GetColor('SceneNodeFocusColor'))
            painter.drawRoundedRect(rect, retRound[0], retRound[1])
    
    #节点上的文字描述
    def paintText(self, painter, text, config):
        size = self.size
        center = QPoint(self.position[0] + size[0]//2, self.position[1])
        scale = config['scale']
        font = DialogSceneSetting.GetFont('SceneNodeFont')
        pointSize = math.ceil(font.pointSize() * scale)
        font.setPointSize(pointSize)
        penWidth = math.ceil(painter.pen().width() * scale)
        #测量渲染出来的文本的包围盒
        fontMetrics = QFontMetrics(font)
        boundingRect = fontMetrics.boundingRect(text)
        boundingRect = QRect(center.x() - boundingRect.width() // 2,
            center.y() - boundingRect.height() // 2,
            boundingRect.width(), boundingRect.height())

        if Config().isDebug():
            #打印包围盒
            color = QColor('#df162a')
            pen = QPen(color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap, Qt.PenJoinStyle.MiterJoin)
            painter.setPen(pen)
            brush = QBrush(color)
            brush.setStyle(Qt.BrushStyle.NoBrush)
            painter.setBrush(brush)
            painter.drawRect(boundingRect)
        
        painter.setFont(font)
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeFontColor'), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawText(boundingRect.bottomLeft() - QPoint(0, penWidth), text)
    
    #绘制节点的注释文本
    def paintCommentText(self, painter, config):
        text = Controller.GetModelItemData(self.modelPath, self.id).get('comment', '')
        if not text:
            return
        size = self.size
        center = QPoint(self.position[0] + size[0]//2, self.position[1])
        scale = config['scale']
        font = DialogSceneSetting.GetFont('SceneNodeFont')
        pointSize = math.ceil(font.pointSize() / 1.3 * scale)
        font.setPointSize(pointSize)
        penWidth = math.ceil(painter.pen().width() * scale)
        #测量渲染出来的文本的包围盒
        fontMetrics = QFontMetrics(font)
        boundingRect = fontMetrics.boundingRect(text)
        center = QPoint(center.x(), center.y() + size[1]//2 - boundingRect.height()//2)
        boundingRect = QRect(center.x() - boundingRect.width() // 2,
            center.y() - boundingRect.height() // 2,
            boundingRect.width(), boundingRect.height())
        
        if Config().isDebug():
            #打印包围盒
            color = QColor('#ce4ddf')
            pen = QPen(color, 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap, Qt.PenJoinStyle.MiterJoin)
            painter.setPen(pen)
            brush = QBrush(color)
            brush.setStyle(Qt.BrushStyle.NoBrush)
            painter.setBrush(brush)
            painter.drawRect(boundingRect)
        
        painter.setFont(font)
        pen = QPen(DialogSceneSetting.GetColor('SceneNodeCommentFontColor'), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawText(boundingRect.bottomLeft() - QPoint(0, penWidth), text)
    
    #绘制错误图标
    def paintError(self, painter):
        if self.checkDrawFlag(SceneNodeDrawFlag.Error):
            #画个红叉叉
            size = self.size
            sx, sy = self.position[0], self.position[1] - size[1]//2
            pen = QPen(QColor('red'), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(QPoint(sx + size[0] // 5, sy + size[1] // 6), QPoint(sx + size[0] // 5 * 4, sy + size[1] // 6 * 5))
            painter.drawLine(QPoint(sx + size[0] // 5 * 4, sy + size[1] // 6), QPoint(sx + size[0] // 5, sy + size[1] // 6 * 5))

    def onPaint(self, painter, config):
        '''
        virtual method
        '''
        self.paintConnectedLine(painter)
        self.paintBackground(painter, config)        
        self.paintText(painter, self.getName(), config)
        self.paintCommentText(painter, config)
    
    def paint(self, painter, config):
        if Config().isDebug():
            color = QColor('#aa00ff')
            pen = QPen(color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap, Qt.PenJoinStyle.MiterJoin)
            painter.setPen(pen)
            brush = QBrush(color)
            brush.setStyle(Qt.BrushStyle.NoBrush)
            painter.setBrush(brush)
            geometry = QRect(self.position[0], self.position[1] - self.span[1]//2, self.span[0], self.span[1])
            painter.drawRect(geometry)

        self.onPaint(painter, config)
        self.paintError(painter)
        self.paintOpSigns(painter)
        for subNode in self.children:
            if subNode:
                subNode.paint(painter, config)

    #保存属性面板上的参数，子类重载
    def onStoreDataFromPropertyWidget(self, widget, data):
        '''
        virtual method
        '''
        pass

    #保存属性面板上的参数
    def storeDataFromPropertyWidget(self):
        if int(self.type) == gg.ControlNodeType.Start:
            return
        itemData = Controller.GetModelItemData(self.modelPath, self.id)
        if itemData is None:
            return
        oldData = itemData.copy()
        data = oldData.copy()
        widget = view_gg.PropertyStackedWidget.currentWidget()
        data['comment'] = self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditComment').text()
        data['color'] = self.findOneWidgetInWidget(widget, QComboBox, 'comboBoxColor').currentText()
        self.onStoreDataFromPropertyWidget(widget, data)
        if oldData != data:
            Controller.UpdateModelItemData(self.modelPath, self.id, data)

    #将控件属性数据显示在属性面板上，子类重载
    def onSetupPropertyWidgetData(self, widget, data):
        '''
        virtual method
        '''
        pass

    #将控件属性数据显示在属性面板上
    def setupPropertyWidgetData(self):
        if int(self.type) == gg.ControlNodeType.Start:
            return
        # print('setupPropertyWidgetData', self.modelPath, self.id)
        data = Controller.GetModelItemData(self.modelPath, self.id)
        widget = view_gg.PropertyStackedWidget.currentWidget()
        self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditID').setText(str(self.id))
        self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditComment').setText(data.get('comment', ''))
        self.setComboxCurrentByText(self.findOneWidgetInWidget(widget, QComboBox, 'comboBoxColor'), data.get('color', ''), 'NoColor')
        itemInfo = data_item.Data.get(int(self.type), None)
        if itemInfo:
            view_gg.CommentPlainTextEdit.setPlainText(itemInfo.get('comment', ''))

        self.onSetupPropertyWidgetData(widget, data)

    def findOneWidgetInWidget(self, parent, cls, name):
        lineEditID = parent.findChildren(cls, name)
        if not lineEditID:
            return None
        return lineEditID[0]
    
    def setComboxCurrentByText(self, combox, text, defaultText):
        if not text:
            text = defaultText
        idx = combox.findText(text)
        if idx == -1:
            combox.setCurrentIndex(0)
        else:
            combox.setCurrentIndex(idx)
    
    def onPick(self):
        '''
        virtual method
        '''
        self.setDrawFlag(SceneNodeDrawFlag.Picked)
        self.unsetDrawFlag(SceneNodeDrawFlag.Error)
        view_gg.PropertyStackedWidget.showByItemType(self.type)
        view_gg.PropertyStackedWidget.scenePickNode = self
        self.setupPropertyWidgetData()
    
    def pick(self, pos):
        # self.geometry = QRect()
        # self.span     = [0, 0]
        # self.position = [0, 0]
        geometry = [self.position[0], self.position[1] - self.span[1]//2, self.span[0], self.span[1]]
        if not utils.isPositionInGeometry(pos, geometry):
            return None
        
        if self.pickable():
            geometry = [self.position[0], self.position[1] - self.size[1]//2, self.size[0], self.size[1]]
            if utils.isPositionInGeometry(pos, geometry):
                self.onPick()
                return self
        
        for subNode in self.children:
            if subNode:
                ret = subNode.pick(pos)
                if ret:
                    return ret
        return None
    
    def pickable(self):
        '''
        virtual method
        '''
        return True
    
    def focusable(self):
        '''
        virtual method
        '''
        return True

    def onMouseMove(self, pos):
        geometry = [self.position[0], self.position[1] - self.span[1]//2, self.span[0], self.span[1]]
        if not utils.isPositionInGeometry(pos, geometry):
            return None
        
        if self.focusable():
            geometry = [self.position[0], self.position[1] - self.size[1]//2, self.size[0], self.size[1]]
            if utils.isPositionInGeometry(pos, geometry):
                self.setDrawFlag(SceneNodeDrawFlag.Focused)
                return self
        
        for subNode in self.children:
            if subNode:
                ret = subNode.onMouseMove(pos)
                if ret:
                    return ret
        return None
    
    #判断坐标pos是否在给定的操作符绘制范围内
    def isPosInOpSignDrawRange(self, pos, opSign):
        sx, sy = self.position[0], self.position[1] - self.size[1]//2
        geometry = [0, 0, 0, 0]
        if SceneNodeDrawFlag.OpSignLeft == opSign:
            geometry = [sx, sy, self.size[0] // 6, self.size[1]]
        elif SceneNodeDrawFlag.OpSignCenterUp == opSign:
            geometry = [sx + self.size[0] // 3, sy, self.size[0] // 3, self.size[1] // 5]
        elif SceneNodeDrawFlag.OpSignCenterMiddle == opSign:
            geometry = [sx + self.size[0] // 3, sy + self.size[1] // 5 * 2, self.size[0] // 3, self.size[1] // 5]
        elif SceneNodeDrawFlag.OpSignCenterBotton == opSign:
            geometry = [sx + self.size[0] // 3, sy + self.size[1] // 5 * 4, self.size[0] // 3, self.size[1] // 5]
        elif SceneNodeDrawFlag.OpSignRightUp == opSign:
            geometry = [sx + self.size[0] // 6 * 5, sy, self.size[0] // 6, self.size[1] // 3]
        elif SceneNodeDrawFlag.OpSignRightMiddle == opSign:
            geometry = [sx + self.size[0] // 6 * 5, sy + self.size[1] // 3, self.size[0] // 6, self.size[1] // 3]
        elif SceneNodeDrawFlag.OpSignRightBotton == opSign:
            geometry = [sx + self.size[0] // 6 * 5, sy + self.size[1] // 3 * 2, self.size[0] // 6, self.size[1] // 3]
        elif SceneNodeDrawFlag.OpSignRight == opSign:
            geometry = [sx + self.size[0] // 6 * 5, sy, self.size[0] // 6, self.size[1]]
        return utils.isPositionInGeometry(pos, geometry)
    
    #判断当前pos处于哪个操作符绘制范围
    def getOpSignDrawFlagByPos(self, pos, nodeType):
        '''
        virtual method
        '''
        for s1, s2 in self.canDropOpSign(nodeType).items():
            if self.isPosInOpSignDrawRange(pos, s1):
                return s2
        return None
    
    #根据给定的操作符类型list，返回一一对应的操作符聚焦标签
    def getOpSignsFocusedMap(self, opSigns):
        return dict([(s1, OpSignFocusedMap[s1]) for s1 in opSigns if s1 in OpSignFocusedMap])
    
    #能放置的操作位置，所有控件的相同行为
    def canDropOpSignCommon(self, dropItemType):
        if not self.parent:
            return
        dropItemType = gg.CNT(dropItemType)
        parentItemType = gg.CNT(self.parent.type)
        if parentItemType in (gg.CNT.ExecUntilFalse, gg.CNT.ExecUnitlTrue, gg.CNT.OrderList, gg.CNT.ProbabilisticChoice,
            gg.CNT.RandomChoice, gg.CNT.RandomList, gg.CNT.Weight):
            #父节点是子节点不固定的组合控件，放置的节点是动作类和组合类，则可以往兄弟节点上插入
            if dropItemType in gg.ControlNodeTypeActionsAndCombination:
                return self.getOpSignsFocusedMap([
                    SceneNodeDrawFlag.OpSignCenterUp,
                    SceneNodeDrawFlag.OpSignCenterBotton,
                ])
        elif parentItemType in (gg.CNT.And, gg.CNT.Or):
            #父节点是子节点不固定的条件类节点，放置的节点是bool类或动作，则可以往兄弟节点上插入
            if dropItemType in gg.ControlNodeTypeBools or dropItemType == gg.CNT.Action:
                return self.getOpSignsFocusedMap([
                    SceneNodeDrawFlag.OpSignCenterUp,
                    SceneNodeDrawFlag.OpSignCenterBotton,
                ])
        return {}

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        return {
            SceneNodeDrawFlag.OpSignLeft         : SceneNodeDrawFlag.OpSignFocusedLeft, 
            SceneNodeDrawFlag.OpSignCenterUp     : SceneNodeDrawFlag.OpSignFocusedCenterUp, 
            SceneNodeDrawFlag.OpSignCenterMiddle : SceneNodeDrawFlag.OpSignFocusedCenterMiddle,
            SceneNodeDrawFlag.OpSignCenterBotton : SceneNodeDrawFlag.OpSignFocusedCenterBotton, 
            SceneNodeDrawFlag.OpSignRightUp      : SceneNodeDrawFlag.OpSignFocusedRightUp, 
            SceneNodeDrawFlag.OpSignRightMiddle  : SceneNodeDrawFlag.OpSignFocusedRightMiddle,
            SceneNodeDrawFlag.OpSignRightBotton  : SceneNodeDrawFlag.OpSignFocusedRightBotton, 
            SceneNodeDrawFlag.OpSignRight        : SceneNodeDrawFlag.OpSignFocusedRight,
        }

    #拖动控件路过节点
    def onMouseDragMoveOthers(self, pos, nodeType):
        opSign = self.getOpSignDrawFlagByPos(pos, nodeType)
        if opSign:
            self.setDrawFlag(opSign)
    
    #设置操作提示符的绘制标记
    def setDrawOpSignFlag(self, nodeType):
        for s1, _ in self.canDropOpSign(nodeType).items():
            self.setDrawFlag(s1)

    def onMouseDragMove(self, pos):
        geometry = [self.position[0], self.position[1] - self.span[1]//2, self.span[0], self.span[1]]
        if not utils.isPositionInGeometry(pos, geometry):
            return None
        
        if self.focusable():
            geometry = [self.position[0], self.position[1] - self.size[1]//2, self.size[0], self.size[1]]
            if utils.isPositionInGeometry(pos, geometry):
                nodeType = gg.CurrentControlNode
                self.setDrawFlag(SceneNodeDrawFlag.Focused)
                self.setDrawOpSignFlag(nodeType['type'])
                self.onMouseDragMoveOthers(pos, nodeType['type'])
                return self
        
        for subNode in self.children:
            if subNode:
                ret = subNode.onMouseDragMove(pos)
                if ret:
                    return ret
        return None
    
    def doDropOpSignCenterMiddle(self, itemType):
        '''
        virtual method
        '''
        #替换当前节点
        Controller.CmdReplaceItem(self.modelPath, self.id, itemType)

    def doDropOpSignRight(self, itemType):
        '''
        virtual method
        '''
        Controller.CmdAddItemByIdAndType(self.modelPath, self.id, itemType, 0)

    def doDrop(self, dropNodeInfo, opSign):
        if SceneNodeDrawFlag.OpSignLeft == opSign:
            #在当前选中节点和其父节点之间插入一个节点
            Controller.CmdInsertItemBefore(self.modelPath, self.id, dropNodeInfo['type'])
        elif SceneNodeDrawFlag.OpSignCenterUp == opSign:
            #在当前选中节点之前插入一个节点（兄弟节点）
            Controller.CmdInsertItemPreSibling(self.modelPath, self.id, dropNodeInfo['type'])
        elif SceneNodeDrawFlag.OpSignCenterMiddle == opSign:
            self.doDropOpSignCenterMiddle(dropNodeInfo['type'])
        elif SceneNodeDrawFlag.OpSignCenterBotton == opSign:
            #在当前选中节点之后插入一个节点（兄弟节点）
            Controller.CmdInsertItemNextSibling(self.modelPath, self.id, dropNodeInfo['type'])
        elif SceneNodeDrawFlag.OpSignRightUp == opSign:
            #右边第一个箭头，第一个子节点
            Controller.CmdAddItemByIdAndType(self.modelPath, self.id, dropNodeInfo['type'], 0)
        elif SceneNodeDrawFlag.OpSignRightMiddle == opSign:
            #右边第二个箭头，第二个子节点
            Controller.CmdAddItemByIdAndType(self.modelPath, self.id, dropNodeInfo['type'], 1)
        elif SceneNodeDrawFlag.OpSignRightBotton == opSign:
            #右边第三个箭头，第三个子节点
            Controller.CmdAddItemByIdAndType(self.modelPath, self.id, dropNodeInfo['type'], 2)
        elif SceneNodeDrawFlag.OpSignRight == opSign:
            self.doDropOpSignRight(dropNodeInfo['type'])

    def onDrop(self, dropNodeInfo, pos):
        geometry = [self.position[0], self.position[1] - self.span[1]//2, self.span[0], self.span[1]]
        if not utils.isPositionInGeometry(pos, geometry):
            return None
        
        if self.focusable():
            geometry = [self.position[0], self.position[1] - self.size[1]//2, self.size[0], self.size[1]]
            if utils.isPositionInGeometry(pos, geometry):
                for opSign, _ in self.canDropOpSign(dropNodeInfo['type']).items():
                    if self.isPosInOpSignDrawRange(pos, opSign):
                        self.doDrop(dropNodeInfo, opSign)
                        # Controller.GetModel(self.modelPath).dump()
                        return True
        
        for subNode in self.children:
            if subNode:
                ret = subNode.onDrop(dropNodeInfo, pos)
                if ret:
                    return ret
        return None
