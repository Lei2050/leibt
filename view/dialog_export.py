from PyQt6.QtWidgets import QDialog, QFileDialog

import view.utils as utils

class DialogExport(QDialog):
    def __init__(self, parent = None, params = {}):
        super(QDialog, self).__init__(parent)
        self.ui = utils.SetupWidgetUI(self, 'dialog_export', 'DialogExport')

        self.ui.pushButtonChooseWorkspaceExportDirectory.clicked.connect(self._chooseWorkspaceExportDirectory)
        
        self.ui.lineEditWorkspaceExportDirectory.setText(params.get('export_directory', ''))
    
    def getParams(self):
        return {
            'code': self.ui.comboBoxCodeType.currentText(),
            'export_directory': self.ui.lineEditWorkspaceExportDirectory.text().rstrip('/\\'),
        }
        
    def _chooseWorkspaceExportDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "请选择目录", "/")
        if not directory:
            return
        self.ui.lineEditWorkspaceExportDirectory.setText(directory)
    