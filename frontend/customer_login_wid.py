# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customer_login_wid.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 360)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.bt_back = QtWidgets.QPushButton(Form)
        self.bt_back.setObjectName("bt_back")
        self.horizontalLayout_5.addWidget(self.bt_back)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_5.setStretch(0, 5)
        self.horizontalLayout_5.setStretch(1, 10)
        self.horizontalLayout_5.setStretch(2, 15)
        self.horizontalLayout_5.setStretch(3, 20)
        self.horizontalLayout_5.setStretch(4, 30)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.le_name = QtWidgets.QLineEdit(Form)
        self.le_name.setInputMethodHints(QtCore.Qt.ImhNone)
        self.le_name.setMaxLength(30)
        self.le_name.setObjectName("le_name")
        self.horizontalLayout_2.addWidget(self.le_name)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_2.setStretch(0, 20)
        self.horizontalLayout_2.setStretch(1, 10)
        self.horizontalLayout_2.setStretch(2, 2)
        self.horizontalLayout_2.setStretch(3, 15)
        self.horizontalLayout_2.setStretch(4, 20)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.le_tableno = QtWidgets.QLineEdit(Form)
        self.le_tableno.setMaxLength(3)
        self.le_tableno.setObjectName("le_tableno")
        self.horizontalLayout_3.addWidget(self.le_tableno)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.horizontalLayout_3.setStretch(0, 20)
        self.horizontalLayout_3.setStretch(1, 10)
        self.horizontalLayout_3.setStretch(2, 2)
        self.horizontalLayout_3.setStretch(3, 15)
        self.horizontalLayout_3.setStretch(4, 20)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem11)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem12)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem13)
        self.le_phone = QtWidgets.QLineEdit(Form)
        self.le_phone.setInputMethodHints(QtCore.Qt.ImhNone)
        self.le_phone.setMaxLength(10)
        self.le_phone.setObjectName("le_phone")
        self.horizontalLayout_6.addWidget(self.le_phone)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem14)
        self.horizontalLayout_6.setStretch(0, 20)
        self.horizontalLayout_6.setStretch(1, 10)
        self.horizontalLayout_6.setStretch(2, 2)
        self.horizontalLayout_6.setStretch(3, 15)
        self.horizontalLayout_6.setStretch(4, 20)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem15)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem16)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem17)
        self.le_mail = QtWidgets.QLineEdit(Form)
        self.le_mail.setMaxLength(50)
        self.le_mail.setObjectName("le_mail")
        self.horizontalLayout_7.addWidget(self.le_mail)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem18)
        self.horizontalLayout_7.setStretch(0, 20)
        self.horizontalLayout_7.setStretch(1, 10)
        self.horizontalLayout_7.setStretch(2, 2)
        self.horizontalLayout_7.setStretch(3, 15)
        self.horizontalLayout_7.setStretch(4, 20)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem19)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem20)
        self.bt_get_started = QtWidgets.QPushButton(Form)
        self.bt_get_started.setObjectName("bt_get_started")
        self.horizontalLayout_4.addWidget(self.bt_get_started)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem21)
        self.horizontalLayout_4.setStretch(0, 31)
        self.horizontalLayout_4.setStretch(1, 5)
        self.horizontalLayout_4.setStretch(2, 15)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem22 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem22)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 25)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout.setStretch(4, 5)
        self.verticalLayout.setStretch(5, 2)
        self.verticalLayout.setStretch(6, 5)
        self.verticalLayout.setStretch(7, 2)
        self.verticalLayout.setStretch(8, 5)
        self.verticalLayout.setStretch(9, 2)
        self.verticalLayout.setStretch(10, 5)
        self.verticalLayout.setStretch(11, 25)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.bt_back.setText(_translate("Form", "Back"))
        self.label_3.setText(_translate("Form", "Customer Login"))
        self.label.setText(_translate("Form", "Name : "))
        self.label_2.setText(_translate("Form", "Table No. : "))
        self.label_4.setText(_translate("Form", "Phone : "))
        self.label_5.setText(_translate("Form", "Mail Id : "))
        self.bt_get_started.setText(_translate("Form", "Get Started"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
