# Form implementation generated from reading ui file 'widget_condition_property.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(213, 122)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxProperty = QtWidgets.QGroupBox(Form)
        self.groupBoxProperty.setObjectName("groupBoxProperty")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxProperty)
        self.formLayout.setObjectName("formLayout")
        self.labelLeftParam = QtWidgets.QLabel(self.groupBoxProperty)
        self.labelLeftParam.setObjectName("labelLeftParam")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelLeftParam)
        self.lineEditLeftParam = QtWidgets.QLineEdit(self.groupBoxProperty)
        self.lineEditLeftParam.setObjectName("lineEditLeftParam")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditLeftParam)
        self.labelOperator = QtWidgets.QLabel(self.groupBoxProperty)
        self.labelOperator.setObjectName("labelOperator")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelOperator)
        self.comboBoxOperator = QtWidgets.QComboBox(self.groupBoxProperty)
        self.comboBoxOperator.setEditable(False)
        self.comboBoxOperator.setObjectName("comboBoxOperator")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBoxOperator)
        self.labelRightParam = QtWidgets.QLabel(self.groupBoxProperty)
        self.labelRightParam.setObjectName("labelRightParam")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelRightParam)
        self.lineEditRightParam = QtWidgets.QLineEdit(self.groupBoxProperty)
        self.lineEditRightParam.setObjectName("lineEditRightParam")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditRightParam)
        self.gridLayout.addWidget(self.groupBoxProperty, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBoxProperty.setTitle(_translate("Form", "??????"))
        self.labelLeftParam.setText(_translate("Form", "?????????"))
        self.labelOperator.setText(_translate("Form", "?????????"))
        self.comboBoxOperator.setCurrentText(_translate("Form", "=="))
        self.comboBoxOperator.setItemText(0, _translate("Form", "=="))
        self.comboBoxOperator.setItemText(1, _translate("Form", "!="))
        self.comboBoxOperator.setItemText(2, _translate("Form", "<"))
        self.comboBoxOperator.setItemText(3, _translate("Form", "<="))
        self.comboBoxOperator.setItemText(4, _translate("Form", ">"))
        self.comboBoxOperator.setItemText(5, _translate("Form", ">="))
        self.labelRightParam.setText(_translate("Form", "?????????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
