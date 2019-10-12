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
        self.lb_name = QtWidgets.QLabel(Form)
        self.lb_name.setObjectName("lb_name")
        self.horizontalLayout_2.addWidget(self.lb_name)
        self.lb_table_no = QtWidgets.QLabel(Form)
        self.lb_table_no.setObjectName("lb_table_no")
        self.horizontalLayout_2.addWidget(self.lb_table_no)
        self.lb_status = QtWidgets.QLabel(Form)
        self.lb_status.setObjectName("lb_status")
        self.horizontalLayout_2.addWidget(self.lb_status)
        self.lb_total = QtWidgets.QLabel(Form)
        self.lb_total.setObjectName("lb_total")
        self.horizontalLayout_2.addWidget(self.lb_total)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.bt_print = QtWidgets.QPushButton(Form)
        self.bt_print.setObjectName("bt_print")
        self.horizontalLayout_2.addWidget(self.bt_print)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.bt_pay = QtWidgets.QPushButton(Form)
        self.bt_pay.setObjectName("bt_pay")
        self.horizontalLayout_2.addWidget(self.bt_pay)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_2.setStretch(4, 1)
        self.horizontalLayout_2.setStretch(5, 1)
        self.horizontalLayout_2.setStretch(6, 1)
        self.horizontalLayout_2.setStretch(7, 1)
        self.horizontalLayout_2.setStretch(8, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lb_name.setText(_translate("Form", "Name"))
        self.lb_table_no.setText(_translate("Form", "Table No."))
        self.lb_status.setText(_translate("Form", "Status"))
        self.lb_total.setText(_translate("Form", "Total"))
        self.bt_print.setText(_translate("Form", "Bill Print"))
        self.bt_pay.setText(_translate("Form", "Payment Done"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
