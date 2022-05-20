from PyQt6.QtWidgets import QWidget, QToolButton
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen, QIcon, QCloseEvent
from PyQt6.QtCore import QPoint, QSize, Qt, QRect

import g.gg as gg
import view.gg as view_gg
from controller.controller import Controller
import view.scene_tree_nodes.scene_node as scene_node
import view.scene_tree_nodes.factory as factory
from view.dialog_scene_setting import DialogSceneSetting
import view.actions as actions
from g.config import Config

import data.error as error

class SceneTree:
    def __init__(self, modelPath):
        self.root = None
        self.modelPath = modelPath

        self.nodes = {}
    
    #返回被选中的节点SceneNode
    def pick(self, pos):
        if not self.root:
            return None
        return self.root.pick(pos)

    def dump(self):
        if not self.root:
            return
        self.root.dump(0)

    def __genTreeNodeByModelItemData(self, modelPath, modelItemData):
        if not modelItemData:
            return
        snode = factory.Factory.New(modelItemData.id, modelItemData.itemType)
        snode.modelPath = modelPath
        self.nodes[snode.id] = snode
        for subItem in modelItemData.getChildren():
            if subItem:
                node = self.__genTreeNodeByModelItemData(modelPath, subItem)
                snode.addChild(node)
                node.parent = snode
            else:
                snode.addChild(None)
        return snode
    
    def paint(self, painter, config):
        pen = QPen()
        pen.setWidth(gg.PainterPenWidth)
        pen.setColor(QColor('green'))
        painter.setPen(pen)
        self.root.paint(painter, config)
    
    #重新结算大小
    def calSize(self, config):
        self.root.calSize(config)

    #重新生成树
    def regenTree(self, config):
        modelData = Controller.GetModel(self.modelPath)
        self.nodes = {}
        self.root = self.__genTreeNodeByModelItemData(self.modelPath, modelData.root)
        self.root.calSize(config)
        offset = config.get('global_offset', (0, 0))
        self.root.calLocation(offset, config)
    
    def onMouseMove(self, pos):
        if not self.root:
            return None
        return self.root.onMouseMove(pos)

    def onMouseDragMove(self, pos):
        if not self.root:
            return None
        return self.root.onMouseDragMove(pos)
    
    def onDrop(self, dropNodeInfo, pos):
        if not self.root:
            return None
        return self.root.onDrop(dropNodeInfo, pos)
    
    def getNode(self, id):
        return self.nodes.get(id, None)

    def span(self):
        return tuple(self.root.span)

class WidgetScene(QWidget):
    def __init__(self, modelPath):
        QWidget.__init__(self)
        self.setAcceptDrops(True)
        #modelPath是目录或行为树相对与工作区的路径，也作为一个行为树的唯一表示
        #view通过向controller传递modelPath来获取行为树的model数据，
        #外部如果有改动modelPath的需求，请调用setModelPath()
        self.modelPath = modelPath
        #当前缩放比列
        self.scale = 1.0
        self.paintOffset = QPoint(0, 0)
        self.toolButtonSize = QSize(32, 32) #左上、右上按钮大小
        self.toolButtonMarginsToEdge = QSize(16, 16) #按钮距离边缘的距离
        self.paintOffset = QPoint(self.toolButtonMarginsToEdge.width(),
            self.toolButtonMarginsToEdge.height() * 2 + self.toolButtonSize.height())
        self.oldMovePos = None
        self.tree = SceneTree(self.modelPath)

        self.leftMousePressed = False
        self.pickedNode = None
        self.lastFocusedNode = None

        self.setMouseTracking(True)

        view_gg.PropertyStackedWidget.RepaintScene.connect(self.update)

        self.setupToolButtons()
        
        #从软件配置中加载该行为树的相关配置
        cfg = Config().loadTreeCfg(self.modelPath)
        self.scale = cfg.get('scale', self.scale)
        po = cfg.get('global_offset', None)
        if po:
            self.paintOffset = QPoint(po[0], po[1])
        self.tree.regenTree(self.getConfig())
    
    def getWorkspaceName(self):
        return self.modelPath[0]
    
    def setModelPath(self, modelPath):
        modelPath = modelPath.copy()
        self.modelPath = modelPath
        self.tree.modelPath = self.modelPath
        self.repaintTree()

    def dragEnterEvent(self, enterEvent):
        enterEvent.acceptProposedAction()

    def dragMoveEvent(self, dragMoveEvent):
        if gg.CurrentControlNode['type'] <= 0:
            return
        pos = dragMoveEvent.position()
        pos = [int(pos.x()), int(pos.y())]
        if self.lastFocusedNode:
            self.lastFocusedNode.unfocused()
        focusedNode = self.tree.onMouseDragMove(pos)
        self.lastFocusedNode = focusedNode

        self.update()

        dragMoveEvent.acceptProposedAction()

    def dropEvent(self, dropEvent):
        # print('=============================================================================')
        # print(gg.CurrentControlNode)
        if gg.CurrentControlNode['type'] <= 0:
            print('not valid node type')
            return
        # print(dir(dropEvent))
        pos = dropEvent.position()
        pos = [int(pos.x()), int(pos.y())]
        if self.lastFocusedNode:
            self.lastFocusedNode.unfocused()
        if self.tree.onDrop(gg.CurrentControlNode, pos):
            self.repaintTree()
        else:
            self.update()
        
        view_gg.PropertyStackedWidget.showEmpty()
    
    def resizeEvent(self, resizeEvent):
        self.adjustToolButtons()
           
    def getConfig(self):
        return {
            'scale': self.scale,
            'node_size': (int(gg.ControlNodeDefaultSize[0] * self.scale), int(gg.ControlNodeDefaultSize[1] * self.scale)),
            'margin': (int(gg.ControlNodeMargin[0] * self.scale), int(gg.ControlNodeMargin[1] * self.scale)),
            'rect_round': (int(gg.ControlNodeRectRound[0] * self.scale), int(gg.ControlNodeRectRound[1] * self.scale)),
            'global_offset': (self.paintOffset.x(), self.paintOffset.y()),
        }
    
    #保存配置到软件配置，落地
    def saveConfigToDisk(self):
        cfg = {
            'scale': self.scale,
            'global_offset': (self.paintOffset.x(), self.paintOffset.y()),
        }
        Config().saveTreeCfg(self.modelPath, cfg)
    
    #重新绘制树，会重新计算节点大小、重新生成树，所以会清掉所有节点的状态
    #如果单纯的通知空间重新绘制，请用self.update()
    def repaintTree(self):
        self.tree.regenTree(self.getConfig())
        self.update()

    def paintEvent(self, paintEvent):
        w, h = self.width(), self.height()
        pixmap = QPixmap(w, h)
        painter = QPainter()
        painter.begin(pixmap)

        painter.fillRect(QRect(0, 0, w, h), DialogSceneSetting.GetColor('SceneBGColor'))
        self.tree.paint(painter, self.getConfig())

        painter.end()

        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(QPoint(0, 0), pixmap)
        qp.end()
    
    def zoomInOrOut(self, inOrOut = True):
        delta = 0.2
        old = self.scale
        self.scale += delta if inOrOut else -delta
        minScale, maxScale = 0.1, 6.0
        if self.scale < minScale:
            self.scale = minScale
        if self.scale > maxScale:
            self.scale = maxScale
        if old != self.scale:
            self.saveConfigToDisk()
            self.repaintTree()

    def wheelEvent(self, wheelEvent):
        # pixelDelta = wheelEvent.pixelDelta()
        numDegrees = wheelEvent.angleDelta()
        self.zoomInOrOut(numDegrees.y() > 0)

        wheelEvent.accept()
    
    def mousePressEvent(self, mouseEvent):
        pos = mouseEvent.pos()
        pos = (pos.x(), pos.y())
        buttons = mouseEvent.buttons()
        if buttons == Qt.MouseButton.LeftButton:
            update = False
            node = self.tree.pick(pos)
            if self.pickedNode is not None and self.pickedNode != node:
                self.pickedNode.unsetDrawFlag(scene_node.SceneNodeDrawFlag.Picked)
                update = True
            self.pickedNode = node
            if not self.pickedNode:
                self.leftMousePressed = True
                self.oldMovePos = mouseEvent.pos()
                view_gg.PropertyStackedWidget.showEmpty()
            else:
                # print('==============', self.pickedNode.id, self.pickedNode.type)
                # self.repaintTree()
                update = True
            
            if update:
                self.update()

        mouseEvent.accept()
    
    def mouseReleaseEvent(self, mouseEvent):
        self.leftMousePressed = False
        mouseEvent.accept()

    def mouseMoveEvent(self, mouseEvent):
        repaint = 0
        pos = mouseEvent.pos()
        if self.leftMousePressed:
            #拖动整个画布，
            # print(pos, self.oldMovePos)
            deltaPoint = pos - self.oldMovePos
            self.paintOffset = self.paintOffset + deltaPoint
            self.oldMovePos = pos
            repaint = 1
            # self.repaintTree()
        else:
            #单纯移动鼠标
            focusedNode = self.tree.onMouseMove([pos.x(), pos.y()])
            # print('=', focusedNode)
            if focusedNode != self.lastFocusedNode:
                if self.lastFocusedNode:
                    self.lastFocusedNode.unsetDrawFlag(scene_node.SceneNodeDrawFlag.Focused)
                    self.lastFocusedNode = None
            self.lastFocusedNode = focusedNode
            repaint = 2

        if repaint == 1:
            self.saveConfigToDisk()
            self.repaintTree()
        elif repaint == 2:
            self.update()

        mouseEvent.accept()
    
    def enterEvent(self, enterEvent):
        self.leftMousePressed = False
        enterEvent.accept()
    
    def leaveEvent(self, event):
        self.leftMousePressed = False
        event.accept()

    # def keyPressEvent(self, keyEvent):
    #     super(WidgetScene, self).keyPressEvent(keyEvent)

    #     print('333333333')

    #     if keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_Z):
    #         print('undo')
    #         # Controller.Undo(self.modelPath)
    #     elif keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_Shift and Qt.Key.Key_Z):
    #         print('redo')
    #         # Controller.Redo(self.modelPath)
        
    #     keyEvent.accept()
    
    #不知为啥，上面的keyPressEvent接收不到按钮时间，在MainWindow中keyPressEvent倒是可以。
    #现在就是在MainWindow中触发信号，调用TabWidgetScene.onKeyPress，然后再调用这里的onKeyPress。
    #TreeViewControl那边的keyPressEvent调用了event.ignore()，否则事件被截断了，暂时这么解决。
    #有些时候按键接收不到，可能是因为焦点不在当前widget
    def onKeyPress(self, keyEvent):
        if keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_Z):
            Controller.Undo(self.modelPath)
            self.repaintTree()
        elif keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_A):
            Controller.Redo(self.modelPath)
            self.repaintTree()
        elif keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_E):
            actions.ActionExportTree(self.modelPath)
        elif keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_C):
            self._onCtrlCCopy()
        elif keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_V):
            self._onCtrlVPaste()
        elif keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_X):
            self._onCtrlXCopy()
        elif keyEvent.key() == (Qt.Key.Key_Control and Qt.Key.Key_S):
            actions.ActionSaveTree(self.modelPath)
        elif keyEvent.key() == Qt.Key.Key_Delete:
            if self.pickedNode:
                Controller.CmdDelete(self.modelPath, self.pickedNode.id)
                self.repaintTree()
                view_gg.PropertyStackedWidget.showEmpty()
        # Controller.GetModel(self.modelPath).dump()

    def showErrors(self, errors):
        path = gg.getPathFromList(self.modelPath)
        if errors:
            view_gg.ClearInfoPlainTextEdit()
            view_gg.InfoPlainTextEditAppenText(path + '行为树有错误')
            for id, errCode in errors:
                node = self.tree.getNode(id)
                if not node:
                    continue
                node.setDrawFlag(scene_node.SceneNodeDrawFlag.Error)
                text = '节点ID：' + str(id) + ', ' + error.Data.get(errCode, '')
                view_gg.InfoPlainTextEditAppenText(text)
            self.update()
        else:
            view_gg.InfoPlainTextEditAppenText(path + '行为树检查通过！')
    
    def _onZoomIn(self):
        self.zoomInOrOut(True)
    
    def _onZoomOut(self):
        self.zoomInOrOut(False)
    
    def _onCheckError(self):
        errs = Controller.ModelCheckModelError(self.modelPath)
        self.showErrors(errs)

    def _onMoveUp(self):
        if not self.pickedNode:
            return
        id = self.pickedNode.id
        Controller.CmdSwapSibling(self.modelPath, self.pickedNode.id, True)
        self.repaintTree()
        node = self.tree.getNode(id)
        if node:
            self.pickedNode = node
            self.pickedNode.onPick()
            self.update()

    def _onMoveDown(self):
        if not self.pickedNode:
            return
        id = self.pickedNode.id
        Controller.CmdSwapSibling(self.modelPath, self.pickedNode.id, False)
        self.repaintTree()
        node = self.tree.getNode(id)
        if node:
            self.pickedNode = node
            self.pickedNode.onPick()
            self.update()
    
    #复制节点
    def _onCtrlCCopy(self):
        if not self.pickedNode:
            return
        actions.ActionCopyModelItem(self.modelPath, self.pickedNode.id)

    #粘贴节点
    def _onCtrlVPaste(self):
        if not self.pickedNode:
            return
        actions.ActionPasteModelItem(self.modelPath, self.pickedNode.id)
        self.repaintTree()

    #剪切节点
    def _onCtrlXCopy(self):
        if not self.pickedNode:
            return
        actions.ActionCutModelItem(self.modelPath, self.pickedNode.id)
        self.repaintTree()
    
    #视图居中
    def _onCenterView(self):
        #先按未缩放的状态计算一下树的视图大小
        self.scale = 1.0
        self.tree.calSize(self.getConfig())
        span = self.tree.span()

        sceneSize = self.size()
        sceneSize = (sceneSize.width() - self.toolButtonMarginsToEdge.width() * 2,
            sceneSize.height() - self.toolButtonMarginsToEdge.height() * 3 - self.toolButtonSize.height())
        ratio1 = span[0] / span[1]
        ratio2 = sceneSize[0] / sceneSize[1]
        l1, l2 = span[0], sceneSize[0]
        if ratio1 < ratio2:
            l1, l2 = span[1], sceneSize[1]
        self.scale *= l2 / l1
        #再计算一下缩放后的树的视图大小
        self.tree.calSize(self.getConfig())
        span = self.tree.span()

        self.paintOffset = QPoint(self.toolButtonMarginsToEdge.width(),
            self.toolButtonMarginsToEdge.height() * 2 + self.toolButtonSize.height())
        if sceneSize[1] > span[1]:
            #y方向完美居中
            self.paintOffset += QPoint(0, (sceneSize[1] - span[1]) // 2)
        self.saveConfigToDisk()
        self.repaintTree()
    
    def setupToolButtons(self):
        buttonSize = self.toolButtonSize

        self.centerViewToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'center.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.centerViewToolButton.setIcon(icon)
        self.centerViewToolButton.setIconSize(buttonSize)
        self.centerViewToolButton.setObjectName("centerViewToolButton")
        self.centerViewToolButton.setToolTip('视图居中')
        self.centerViewToolButton.clicked.connect(self._onCenterView)
        self.zoomInToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'zoom_in.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoomInToolButton.setIcon(icon)
        self.zoomInToolButton.setIconSize(buttonSize)
        self.zoomInToolButton.setObjectName("zoomInToolButton")
        self.zoomInToolButton.setToolTip('放大')
        self.zoomInToolButton.clicked.connect(self._onZoomIn)
        self.zoomOutToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'zoom_out.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoomOutToolButton.setIcon(icon)
        self.zoomOutToolButton.setIconSize(buttonSize)
        self.zoomOutToolButton.setObjectName("zoomOutToolButton")
        self.zoomOutToolButton.setToolTip('缩小')
        self.zoomOutToolButton.clicked.connect(self._onZoomOut)

        self.topLeftToolButtons = [self.centerViewToolButton, self.zoomInToolButton, self.zoomOutToolButton]

        self.moveUpToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'move_up.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.moveUpToolButton.setIcon(icon)
        self.moveUpToolButton.setIconSize(buttonSize)
        self.moveUpToolButton.setObjectName("moveUpToolButton")
        self.moveUpToolButton.setToolTip('上移')
        self.moveUpToolButton.clicked.connect(self._onMoveUp)
        self.moveDownToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'move_down.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.moveDownToolButton.setIcon(icon)
        self.moveDownToolButton.setIconSize(buttonSize)
        self.moveDownToolButton.setObjectName("moveDownToolButton")
        self.moveDownToolButton.setToolTip('下移')
        self.moveDownToolButton.clicked.connect(self._onMoveDown)
        self.saveToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'save.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.saveToolButton.setIcon(icon)
        self.saveToolButton.setIconSize(buttonSize)
        self.saveToolButton.setObjectName("saveToolButton")
        self.saveToolButton.setToolTip('保存')
        self.saveToolButton.clicked.connect(lambda: actions.ActionSaveTree(self.modelPath))
        self.saveAsToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'save_as.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.saveAsToolButton.setIcon(icon)
        self.saveAsToolButton.setIconSize(buttonSize)
        self.saveAsToolButton.setObjectName("saveAsToolButton")
        self.saveAsToolButton.setToolTip('另存为')
        self.saveAsToolButton.clicked.connect(lambda: actions.ActionSaveAsTree(self.modelPath))
        self.exportToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'export.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportToolButton.setIcon(icon)
        self.exportToolButton.setIconSize(buttonSize)
        self.exportToolButton.setObjectName("exportToolButton")
        self.exportToolButton.setToolTip('导出代码')
        self.exportToolButton.clicked.connect(lambda: actions.ActionExportTree(self.modelPath))
        self.checkToolButton = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(gg.IconPrefix + 'check.png'), QIcon.Mode.Normal, QIcon.State.Off)
        self.checkToolButton.setIcon(icon)
        self.checkToolButton.setIconSize(buttonSize)
        self.checkToolButton.setObjectName("checkToolButton")
        self.checkToolButton.setToolTip('错误检查')
        self.checkToolButton.clicked.connect(self._onCheckError)

        self.topRightToolButtons = [self.moveUpToolButton, self.moveDownToolButton, self.saveToolButton,
            self.saveAsToolButton, self.exportToolButton, self.checkToolButton]
    
    def adjustToolButtons(self):
        buttonSize = self.toolButtonSize
        marginsToEdge = self.toolButtonMarginsToEdge
        margin = 8 #按钮间的距离
        # self.sizeHint()
        size = self.size()
        geometry = QRect(marginsToEdge.width(),
            marginsToEdge.height(),
            buttonSize.width(),
            buttonSize.height()) #左边第一个按钮的
        for v in self.topLeftToolButtons:
            v.setGeometry(geometry)
            geometry.setX(geometry.x() + margin + buttonSize.width())
            geometry.setWidth(buttonSize.width())
        
        geometry = QRect(size.width() - marginsToEdge.width() - buttonSize.width(),
            marginsToEdge.height(),
            buttonSize.width(),
            buttonSize.height()) #右边第一个按钮的
        for v in self.topRightToolButtons[::-1]:
            v.setGeometry(geometry)
            geometry.setX(geometry.x() - margin - buttonSize.width())
            geometry.setWidth(buttonSize.width())
    
    #该场景被关闭时
    def onCloseScene(self):
        Config().remTreeCfg(self.modelPath)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.onCloseScene()
        return super().closeEvent(a0)
