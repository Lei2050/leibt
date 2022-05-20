from PyQt6.QtWidgets import QDialog, QFileDialog

import view.utils as utils

class DialogNewWorkspace(QDialog):
    def __init__(self, parent = None, params = {}):
        super(QDialog, self).__init__(parent)
        self.ui = utils.SetupWidgetUI(self, 'dialog_new_workspace', 'DialogNewWorkspace')

        self.ui.pushButtonChooseWorkspaceDirectory.clicked.connect(self._chooseWorkspaceDirectory)
        self.ui.pushButtonChooseWorkspaceExportDirectory.clicked.connect(self._chooseWorkspaceExportDirectory)
        
        self.ui.lineEditWorkspaceName.setText(params.get('name', ''))
        self.ui.lineEditWorkspaceDirectory.setText(params.get('directory', '/'))
        self.ui.lineEditWorkspaceExportDirectory.setText(params.get('export_directory', '/'))
    
    def getParams(self):
        return {
            'name': self.ui.lineEditWorkspaceName.text(),
            'directory': self.ui.lineEditWorkspaceDirectory.text(),
            'export_directory': self.ui.lineEditWorkspaceExportDirectory.text(),
        }
    
    def _chooseWorkspaceDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "请选择目录", "/")
        if not directory:
            return
        self.ui.lineEditWorkspaceDirectory.setText(directory)
    
    def _chooseWorkspaceExportDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "请选择目录", "/")
        if not directory:
            return
        self.ui.lineEditWorkspaceExportDirectory.setText(directory)
    
    def unableChooseDirectory(self):
        self.ui.pushButtonChooseWorkspaceDirectory.setEnabled(False)
    