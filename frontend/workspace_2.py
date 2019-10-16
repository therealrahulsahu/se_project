# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workspace_2.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bt_print = QtWidgets.QPushButton(Dialog)
        self.bt_print.setObjectName("bt_print")
        self.horizontalLayout.addWidget(self.bt_print)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tb_bill = QtWidgets.QTextBrowser(Dialog)
        self.tb_bill.setObjectName("tb_bill")
        self.verticalLayout.addWidget(self.tb_bill)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 20)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.bt_print.setText(_translate("Dialog", "Print"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
