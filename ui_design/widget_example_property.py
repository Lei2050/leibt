# Form implementation generated from reading ui file 'widget_example_property.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(384, 356)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBoxProperty = QtWidgets.QGroupBox(Form)
        self.groupBoxProperty.setObjectName("groupBoxProperty")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBoxProperty)
        self.formLayout_3.setObjectName("formLayout_3")
        self.labelLeftParam = QtWidgets.QLabel(self.groupBoxProperty)
        self.labelLeftParam.setObjectName("labelLeftParam")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelLeftParam)
        self.lineEditLeftParam = QtWidgets.QLineEdit(self.groupBoxProperty)
        self.lineEditLeftParam.setObjectName("lineEditLeftParam")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditLeftParam)
        self.labelOperator = QtWidgets.QLabel(self.groupBoxProperty)
        self.labelOperator.setObjectName("labelOperator")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelOperator)
        self.comboBoxOperator = QtWidgets.QComboBox(self.groupBoxProperty)
        self.comboBoxOperator.setEditable(False)
        self.comboBoxOperator.setObjectName("comboBoxOperator")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.comboBoxOperator.addItem("")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBoxOperator)
        self.labelRightParam = QtWidgets.QLabel(self.groupBoxProperty)
        self.labelRightParam.setObjectName("labelRightParam")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelRightParam)
        self.lineEditRightParam = QtWidgets.QLineEdit(self.groupBoxProperty)
        self.lineEditRightParam.setObjectName("lineEditRightParam")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditRightParam)
        self.verticalLayout.addWidget(self.groupBoxProperty)
        self.groupBoxDebug = QtWidgets.QGroupBox(Form)
        self.groupBoxDebug.setObjectName("groupBoxDebug")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxDebug)
        self.formLayout.setObjectName("formLayout")
        self.labelID = QtWidgets.QLabel(self.groupBoxDebug)
        self.labelID.setObjectName("labelID")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelID)
        self.lineEditID = QtWidgets.QLineEdit(self.groupBoxDebug)
        self.lineEditID.setReadOnly(True)
        self.lineEditID.setObjectName("lineEditID")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditID)
        self.verticalLayout.addWidget(self.groupBoxDebug)
        self.groupBoxComment = QtWidgets.QGroupBox(Form)
        self.groupBoxComment.setObjectName("groupBoxComment")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBoxComment)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelComment = QtWidgets.QLabel(self.groupBoxComment)
        self.labelComment.setObjectName("labelComment")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelComment)
        self.lineEditComment = QtWidgets.QLineEdit(self.groupBoxComment)
        self.lineEditComment.setObjectName("lineEditComment")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditComment)
        self.labelColor = QtWidgets.QLabel(self.groupBoxComment)
        self.labelColor.setObjectName("labelColor")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelColor)
        self.comboBox = QtWidgets.QComboBox(self.groupBoxComment)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBox)
        self.verticalLayout.addWidget(self.groupBoxComment)
        spacerItem = QtWidgets.QSpacerItem(20, 52, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

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
        self.groupBoxDebug.setTitle(_translate("Form", "??????"))
        self.labelID.setText(_translate("Form", "??????ID"))
        self.groupBoxComment.setTitle(_translate("Form", "??????"))
        self.labelComment.setText(_translate("Form", "??????"))
        self.labelColor.setText(_translate("Form", "????????????"))
        self.comboBox.setItemText(0, _translate("Form", "NoColor"))
        self.comboBox.setItemText(1, _translate("Form", "Red"))
        self.comboBox.setItemText(2, _translate("Form", "Yellow"))
        self.comboBox.setItemText(3, _translate("Form", "Blue"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
