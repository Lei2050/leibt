import time

from PyQt6.QtWidgets import QMessageBox

import common.utils as utils

MainWindow = None
PropertyStackedWidget = None
CommentPlainTextEdit = None
InfoPlainTextEdit = None
WorkspaceTreeView = None
SceneTabWidget = None

def InfoPlainTextEditAppenText(text):
    prefix = time.strftime("[%H:%M:%S] ", time.localtime()) 
    InfoPlainTextEdit.appendPlainText(prefix + text)

def ClearInfoPlainTextEdit():
    InfoPlainTextEdit.clear()

def ShowErrorMsgDialog(text):
    QMessageBox.warning(MainWindow, '错误', text, QMessageBox.StandardButton.Yes)

def PrintTraceback():
    InfoPlainTextEditAppenText(utils.getFormatTraceback())
