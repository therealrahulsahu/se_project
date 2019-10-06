# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workspace.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lb_food_name = QtWidgets.QLabel(Form)
        self.lb_food_name.setObjectName("lb_food_name")
        self.horizontalLayout_2.addWidget(self.lb_food_name)
        self.lb_price = QtWidgets.QLabel(Form)
        self.lb_price.setObjectName("lb_price")
        self.horizontalLayout_2.addWidget(self.lb_price)
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_quantity = QtWidgets.QLineEdit(Form)
        self.le_quantity.setInputMethodHints(QtCore.Qt.ImhNone)
        self.le_quantity.setMaxLength(2)
        self.le_quantity.setObjectName("le_quantity")
        self.horizontalLayout_2.addWidget(self.le_quantity)
        self.bt_remove = QtWidgets.QPushButton(Form)
        self.bt_remove.setObjectName("bt_remove")
        self.horizontalLayout_2.addWidget(self.bt_remove)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 4)
        self.horizontalLayout_2.setStretch(2, 2)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_2.setStretch(4, 4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lb_food_name.setText(_translate("Form", "Food Name"))
        self.lb_price.setText(_translate("Form", "Price"))
        self.label.setText(_translate("Form", "Quantity : "))
        self.le_quantity.setText(_translate("Form", "1"))
        self.bt_remove.setText(_translate("Form", "Remove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
