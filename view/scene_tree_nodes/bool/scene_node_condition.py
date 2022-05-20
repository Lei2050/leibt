from PyQt6.QtWidgets import QLineEdit, QComboBox

from view.scene_tree_nodes.scene_node import SceneNodeDrawFlag
import view.scene_tree_nodes.bool.scene_node_bool as scene_node_bool
import controller.controller as controller
import g.gg as gg

class SceneNodeCondition(scene_node_bool.SceneNodeBool):
    def __init__(self, id, type):
        scene_node_bool.SceneNodeBool.__init__(self, id, type)
    
    def onPaint(self, painter, config):
        '''
        virtual method
        '''
        self.paintConnectedLine(painter)
        self.paintBackground(painter, config)   
        
        itemData = controller.Controller.GetModelItemData(self.modelPath, self.id)
        if itemData is None:
            return
        leftParam  = itemData.get('left_param', '')
        operator   = itemData.get('operator', '==')
        rightParam = itemData.get('right_param', '')
        self.paintText(painter, leftParam + ' ' + operator + ' ' +  rightParam, config)
        self.paintCommentText(painter, config)

    #能放置的操作位置
    def canDropOpSign(self, dropItemType):
        '''
        virtual method
        '''
        dit = gg.ControlNodeType(dropItemType)
        ret = {}
        opSigns = []
        if dit in [gg.ControlNodeType.And, gg.ControlNodeType.Or]:
            opSigns.append(SceneNodeDrawFlag.OpSignLeft)
        if dit in gg.ControlNodeTypeBools:
            opSigns.append(SceneNodeDrawFlag.OpSignCenterMiddle)
        ret = self.getOpSignsFocusedMap(opSigns)
        ret.update(self.canDropOpSignCommon(dropItemType))
        return ret
    
    #保存属性面板上的参数，子类执行
    def onStoreDataFromPropertyWidget(self, widget, data):
        '''
        virtual method
        '''
        data['left_param'] = self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditLeftParam').text()
        data['operator'] = self.findOneWidgetInWidget(widget, QComboBox, 'comboBoxOperator').currentText()
        data['right_param'] = self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditRightParam').text()

    #将控件属性数据显示在属性面板上，子类执行
    def onSetupPropertyWidgetData(self, widget, data):
        '''
        virtual method
        '''
        self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditLeftParam').setText(data.get('left_param', ''))
        self.setComboxCurrentByText(self.findOneWidgetInWidget(widget, QComboBox, 'comboBoxOperator'), data.get('operator', ''), '==')
        self.findOneWidgetInWidget(widget, QLineEdit, 'lineEditRightParam').setText(data.get('right_param', ''))
    