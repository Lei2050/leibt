# Form implementation generated from reading ui file 'dialog_export.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogExport(object):
    def setupUi(self, DialogExport):
        DialogExport.setObjectName("DialogExport")
        DialogExport.resize(532, 113)
        self.gridLayout_2 = QtWidgets.QGridLayout(DialogExport)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelCodeType = QtWidgets.QLabel(DialogExport)
        self.labelCodeType.setObjectName("labelCodeType")
        self.gridLayout.addWidget(self.labelCodeType, 0, 0, 1, 1)
        self.comboBoxCodeType = QtWidgets.QComboBox(DialogExport)
        self.comboBoxCodeType.setObjectName("comboBoxCodeType")
        self.comboBoxCodeType.addItem("")
        self.gridLayout.addWidget(self.comboBoxCodeType, 0, 1, 1, 1)
        self.labelWorkspaceExportDirectory = QtWidgets.QLabel(DialogExport)
        self.labelWorkspaceExportDirectory.setObjectName("labelWorkspaceExportDirectory")
        self.gridLayout.addWidget(self.labelWorkspaceExportDirectory, 1, 0, 1, 1)
        self.lineEditWorkspaceExportDirectory = QtWidgets.QLineEdit(DialogExport)
        self.lineEditWorkspaceExportDirectory.setReadOnly(True)
        self.lineEditWorkspaceExportDirectory.setObjectName("lineEditWorkspaceExportDirectory")
        self.gridLayout.addWidget(self.lineEditWorkspaceExportDirectory, 1, 1, 1, 1)
        self.pushButtonChooseWorkspaceExportDirectory = QtWidgets.QPushButton(DialogExport)
        self.pushButtonChooseWorkspaceExportDirectory.setObjectName("pushButtonChooseWorkspaceExportDirectory")
        self.gridLayout.addWidget(self.pushButtonChooseWorkspaceExportDirectory, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogExport)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(DialogExport)
        self.buttonBox.accepted.connect(DialogExport.accept) # type: ignore
        self.buttonBox.rejected.connect(DialogExport.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogExport)

    def retranslateUi(self, DialogExport):
        _translate = QtCore.QCoreApplication.translate
        DialogExport.setWindowTitle(_translate("DialogExport", "Dialog"))
        self.labelCodeType.setText(_translate("DialogExport", "代码类型："))
        self.comboBoxCodeType.setItemText(0, _translate("DialogExport", "python"))
        self.labelWorkspaceExportDirectory.setText(_translate("DialogExport", "导出位置："))
        self.pushButtonChooseWorkspaceExportDirectory.setText(_translate("DialogExport", "浏览..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogExport = QtWidgets.QDialog()
    ui = Ui_DialogExport()
    ui.setupUi(DialogExport)
    DialogExport.show()
    sys.exit(app.exec())
