from PyQt6.QtWidgets import QDialog, QFileDialog, QPushButton, QLabel, QColorDialog, QFontDialog
from PyQt6.QtGui import QFont, QCursor, QMouseEvent, QColor, QCloseEvent
from PyQt6.QtCore import Qt
from g.config import Config

import view.utils as utils
import view.gg as view_gg

Instance = None

class DialogSceneSetting(QDialog):

    DefaultColors = {
        "SceneBGColor": "#1c5555",
        "SceneNodeBGColor": "#009500",
        "SceneNodeCommentFontColor": "#000000",
        "SceneNodeFocusColor": "#00ff7f",
        "SceneNodeFontColor": "#000000",
        "SceneNodeLineColor": "#ffffff",
        "SceneNodeOpSignColor": "#260013",
        "SceneNodeOpSignFocusColor": "#e2e2e2",
        "SceneNodePickedColor": "#ffff00",
        "TreeViewEditingColor": "#00aa00"
    }

    DefaultFont = {
        "SceneNodeFont": "Courier New,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1,Regular",
    }

    def __init__(self, parent = None, params = {}):
        super(QDialog, self).__init__(parent)
        self.ui = utils.SetupWidgetUI(self, 'dialog_scene_setting', 'DialogSceneSetting')

        self.colorLabels = DialogSceneSetting.DefaultColors.copy()
        self.fontLabels = DialogSceneSetting.DefaultFont.copy()

        self.setup()

        global Instance
        Instance = self
    
    def setup(self):
        cfg = Config().loadSceneSetting()

        for k in self.colorLabels.keys():
            cfgVal = cfg.get(k, None)
            if cfgVal:
                self.colorLabels[k] = cfgVal
        
        for k in self.fontLabels.keys():
            cfgVal = cfg.get(k, None)
            if cfgVal:
                self.fontLabels[k] = cfgVal
        
        for k, v in self.colorLabels.items():
            colorLabel = getattr(self.ui, k)
            colorLabel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            #name=(k + '.')[:-1]，复制一份，
            #这么写，确保在生成lambda时就复制name，避免闭包中引用同一个变量
            #下同
            colorLabel.mouseReleaseEvent = lambda ev, name=(k + '.')[:-1]: self.colorLabelMouseReleaseEvent(name, ev)
            colorLabel.setStyleSheet(f'background-color:{v}')
        
        for k, v in self.fontLabels.items():
            fontLabel = getattr(self.ui, k)
            fontLabel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            fontLabel.mouseReleaseEvent = lambda ev, name=(k + '.')[:-1]: self.fontLabelMouseReleaseEvent(name, ev)
            fontLabel.setText(v)

        self.ui.pushButtonApply.clicked.connect(self.apply)
        self.ui.pushButtonCancel.clicked.connect(self.close)

    def colorLabelMouseReleaseEvent(self, name, ev: QMouseEvent):
        color = QColorDialog.getColor(QColor(self.colorLabels[name]))
        if not color.isValid():
            return
        colorName = color.name()
        self.colorLabels[name] = colorName
        colorLabel = getattr(self.ui, name)
        colorLabel.setStyleSheet(f'background-color:{colorName}')
    
    def fontLabelMouseReleaseEvent(self, name: str, ev: QMouseEvent):
        f = QFont()
        f.fromString(self.fontLabels[name])
        font, ok = QFontDialog.getFont(f)
        if not ok:
            return
        fontStr = font.toString()
        self.fontLabels[name] = fontStr
        fontLabel = getattr(self.ui, name)
        fontLabel.setText(fontStr)
    
    def saveConfig(self):
        data = self.colorLabels.copy()
        data.update(self.fontLabels)
        Config().saveSceneSetting(data)

    def apply(self):
        self.saveConfig()
        view_gg.MainWindow.SceneSettingChanged.emit()
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        global Instance
        Instance = None
        return super().closeEvent(a0)
    
    @classmethod
    def GetColor(cls, name: str) -> QColor:
        return QColor(Config().loadSceneSetting().get(name, cls.DefaultColors.get(name, '')))
    
    @classmethod
    def GetFont(cls, name: str) -> QFont:
        fontStr = Config().loadSceneSetting().get(name, cls.DefaultFont.get(name, ''))
        f = QFont()
        f.fromString(fontStr)
        return f
    