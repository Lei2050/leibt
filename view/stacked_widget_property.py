from PyQt6.QtWidgets import QStackedWidget, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QGridLayout
from PyQt6.QtCore import pyqtSignal

import g.gg as gg
import ui_design.widget_common_property_debug as widget_common_property_debug
import ui_design.widget_common_property_comment as widget_common_property_comment
import ui_design.widget_common_property_empty as widget_common_property_empty

from PyQt6.QtCore import QObject
import data.item as data_item

'''
属性面板的StackedWidget
'''
class StackedWidgetProperty(QStackedWidget):
    RepaintScene = pyqtSignal()

    def __init__(self, parent):
        super(QStackedWidget, self).__init__(parent)

        self.propertyWidgets = {}
        #场景中选中的结点，方便写某些逻辑
        self.scenePickNode = None

    def setup(self):
        self.emptyWidget = self.genEmptyWidget()
        # self.emptyWidget.show()
        self.addWidget(self.emptyWidget)
        # self.setCurrentWidget(self.emptyWidget)
    
    def showByItemType(self, itemType):
        if self.scenePickNode:
            self.scenePickNode.storeDataFromPropertyWidget()
            self.RepaintScene.emit()
        
        widget = self.propertyWidgets.get(itemType, None)
        if not widget:
            widget = self.genWidgetByItemType(itemType)
            if not widget:
                self.showEmpty()
                return
            self.addWidget(widget)
            self.propertyWidgets[itemType] = widget
        self.setCurrentWidget(widget)
    
    def showEmpty(self):
        if self.scenePickNode:
            self.scenePickNode.storeDataFromPropertyWidget()
            self.RepaintScene.emit()
        self.scenePickNode = None
        self.setCurrentWidget(self.emptyWidget)

    #根据控件类型生成一个widget
    def genWidgetByItemType(self, itemType):
        if int(itemType) == int(gg.ControlNodeType.Start):
            return self.genEmptyWidget()
        itemData = data_item.Data.get(int(itemType), None)
        if not itemData:
            return None
        retWidget = QWidget()
        retWidget.setObjectName(itemData['name'])
        verticalLayout = QVBoxLayout(retWidget)
        verticalLayout.setObjectName("verticalLayout")

        try:
            path = f"ui_design.widget_{itemData['name']}_property"
            name = f"widget_{itemData['name']}_property"
            # print(path, name)
            module = __import__(path, fromlist=[name, ])
            #return getattr(module, name, None)(compId, entity)
            propertyWidget = self.genWidgetByModule(module)
            verticalLayout.addWidget(propertyWidget)
            setattr(retWidget, 'propertyWidget', propertyWidget)
        except Exception as e:
            # print('empty property')
            pass
        
        debugWidget = self.genDebugWidget()
        verticalLayout.addWidget(debugWidget)
        setattr(retWidget, 'debugWidget', debugWidget)
        commentWidget = self.genCommentWidget()
        verticalLayout.addWidget(commentWidget)
        setattr(retWidget, 'commentWidget', commentWidget)
        spacerItem = QSpacerItem(20, 52, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        verticalLayout.addItem(spacerItem)

        return retWidget
    
    def genWidgetByModule(self, module):
        retWidget = QWidget()
        ui = module.Ui_Form()
        ui.setupUi(retWidget)
        return retWidget

    def genDebugWidget(self):
        ret = self.genWidgetByModule(widget_common_property_debug)
        ret.setObjectName('debug')
        return ret

    def genCommentWidget(self):
        ret = self.genWidgetByModule(widget_common_property_comment)
        ret.setObjectName('commen')
        return ret
    
    def genEmptyWidget(self):
        ret = self.genWidgetByModule(widget_common_property_empty)
        ret.setObjectName('empty')
        return ret
    