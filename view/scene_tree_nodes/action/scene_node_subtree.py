from PyQt6.QtWidgets import QComboBox, QMessageBox

import view.scene_tree_nodes.scene_node as scene_node
import g.gg as gg
from controller.controller import Controller
import view.gg as view_gg

class SceneSubTree(scene_node.SceneNode):
    def __init__(self, id, type):
        scene_node.SceneNode.__init__(self, id, type)

    def onPaint(self, painter, config):
        '''
        virtual method
        '''
        self.paintConnectedLine(painter)
        self.paintBackground(painter, config)   
        
        itemData = Controller.GetModelItemData(self.modelPath, self.id)
        if itemData is None:
            return
        subtree = itemData.get('subtree', '')
        self.paintText(painter, self.getName() + f'({subtree})', config)
        self.paintCommentText(painter, config)
    
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
        data['subtree'] = self.findOneWidgetInWidget(widget, QComboBox, 'comboBoxSubTree').currentText()

    #将控件属性数据显示在属性面板上，子类执行
    def onSetupPropertyWidgetData(self, widget, data):
        '''
        virtual method
        '''
        allSelectablePaths = Controller.ModelGetAllModelPaths(self.getWorkspaceName())
        if isinstance(allSelectablePaths, str):
            QMessageBox.warning(view_gg.MainWindow, '错误', allSelectablePaths, QMessageBox.StandardButton.Yes)
            return
        comboBoxSubTree = self.findOneWidgetInWidget(widget, QComboBox, 'comboBoxSubTree')
        comboBoxSubTree.clear()
        #排除自己的其他所有行为树
        allSelectablePaths = ['/'.join(v) for v in allSelectablePaths if self.modelPath != v]
        comboBoxSubTree.insertItem(0, '')
        comboBoxSubTree.insertItems(1, allSelectablePaths)
        comboBoxSubTree.setCurrentText(data.get('subtree', ''))
    