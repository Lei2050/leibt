# Form implementation generated from reading ui file 'widget_wait_property.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(249, 70)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxProperty = QtWidgets.QGroupBox(Form)
        self.groupBoxProperty.setObjectName("groupBoxProperty")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxProperty)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBoxProperty)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditWaitTime = QtWidgets.QLineEdit(self.groupBoxProperty)
        self.lineEditWaitTime.setObjectName("lineEditWaitTime")
        self.gridLayout.addWidget(self.lineEditWaitTime, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxProperty, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBoxProperty.setTitle(_translate("Form", "属性"))
        self.label.setText(_translate("Form", "等待时间(ms)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())