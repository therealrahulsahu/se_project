# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customer_wid.ui'
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
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rbt_veg = QtWidgets.QRadioButton(self.tab)
        self.rbt_veg.setObjectName("rbt_veg")
        self.horizontalLayout_2.addWidget(self.rbt_veg)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gp_region = QtWidgets.QGroupBox(self.tab)
        self.gp_region.setObjectName("gp_region")
        self.gridLayout = QtWidgets.QGridLayout(self.gp_region)
        self.gridLayout.setObjectName("gridLayout")
        self.rbt_rajas = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_rajas.setObjectName("rbt_rajas")
        self.gridLayout.addWidget(self.rbt_rajas, 2, 2, 1, 1)
        self.rbt_thai = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_thai.setObjectName("rbt_thai")
        self.gridLayout.addWidget(self.rbt_thai, 2, 0, 1, 1)
        self.rbt_north_ind = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_north_ind.setChecked(True)
        self.rbt_north_ind.setObjectName("rbt_north_ind")
        self.gridLayout.addWidget(self.rbt_north_ind, 0, 0, 1, 1)
        self.rbt_china = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_china.setObjectName("rbt_china")
        self.gridLayout.addWidget(self.rbt_china, 2, 1, 1, 1)
        self.rbt_italian = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_italian.setObjectName("rbt_italian")
        self.gridLayout.addWidget(self.rbt_italian, 0, 1, 1, 1)
        self.rbt_south_ind = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_south_ind.setObjectName("rbt_south_ind")
        self.gridLayout.addWidget(self.rbt_south_ind, 0, 2, 1, 1)
        self.rbt_conti = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_conti.setObjectName("rbt_conti")
        self.gridLayout.addWidget(self.rbt_conti, 0, 3, 1, 1)
        self.rbt_none = QtWidgets.QRadioButton(self.gp_region)
        self.rbt_none.setChecked(False)
        self.rbt_none.setObjectName("rbt_none")
        self.gridLayout.addWidget(self.rbt_none, 2, 3, 1, 1)
        self.horizontalLayout_4.addWidget(self.gp_region)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gp_type = QtWidgets.QGroupBox(self.tab)
        self.gp_type.setObjectName("gp_type")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gp_type)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rbt_main = QtWidgets.QRadioButton(self.gp_type)
        self.rbt_main.setObjectName("rbt_main")
        self.gridLayout_2.addWidget(self.rbt_main, 3, 0, 1, 1)
        self.rbt_refresh = QtWidgets.QRadioButton(self.gp_type)
        self.rbt_refresh.setObjectName("rbt_refresh")
        self.gridLayout_2.addWidget(self.rbt_refresh, 0, 1, 1, 1)
        self.rbt_dessert = QtWidgets.QRadioButton(self.gp_type)
        self.rbt_dessert.setObjectName("rbt_dessert")
        self.gridLayout_2.addWidget(self.rbt_dessert, 3, 1, 1, 1)
        self.rbt_starter = QtWidgets.QRadioButton(self.gp_type)
        self.rbt_starter.setChecked(True)
        self.rbt_starter.setObjectName("rbt_starter")
        self.gridLayout_2.addWidget(self.rbt_starter, 0, 0, 1, 1)
        self.rbt_bread = QtWidgets.QRadioButton(self.gp_type)
        self.rbt_bread.setObjectName("rbt_bread")
        self.gridLayout_2.addWidget(self.rbt_bread, 0, 2, 1, 1)
        self.horizontalLayout_3.addWidget(self.gp_type)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.bt_get = QtWidgets.QPushButton(self.tab)
        self.bt_get.setObjectName("bt_get")
        self.horizontalLayout_5.addWidget(self.bt_get)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem6)
        self.scrollarea1 = QtWidgets.QScrollArea(self.tab)
        self.scrollarea1.setWidgetResizable(True)
        self.scrollarea1.setObjectName("scrollarea1")
        self.ScrollLay = QtWidgets.QWidget()
        self.ScrollLay.setGeometry(QtCore.QRect(0, 0, 299, 104))
        self.ScrollLay.setObjectName("ScrollLay")
        self.scroll_choose = QtWidgets.QVBoxLayout(self.ScrollLay)
        self.scroll_choose.setObjectName("scroll_choose")
        self.scrollarea1.setWidget(self.ScrollLay)
        self.verticalLayout_5.addWidget(self.scrollarea1)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 4)
        self.verticalLayout_5.setStretch(2, 1)
        self.verticalLayout_5.setStretch(3, 8)
        self.verticalLayout_5.setStretch(4, 1)
        self.verticalLayout_5.setStretch(5, 8)
        self.verticalLayout_5.setStretch(6, 1)
        self.verticalLayout_5.setStretch(7, 4)
        self.verticalLayout_5.setStretch(8, 1)
        self.verticalLayout_5.setStretch(9, 60)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem7)
        self.scrollarea2 = QtWidgets.QScrollArea(self.tab)
        self.scrollarea2.setWidgetResizable(True)
        self.scrollarea2.setObjectName("scrollarea2")
        self.scroll_lay2 = QtWidgets.QWidget()
        self.scroll_lay2.setGeometry(QtCore.QRect(0, 0, 299, 247))
        self.scroll_lay2.setObjectName("scroll_lay2")
        self.scroll_select = QtWidgets.QVBoxLayout(self.scroll_lay2)
        self.scroll_select.setObjectName("scroll_select")
        self.scrollarea2.setWidget(self.scroll_lay2)
        self.verticalLayout_3.addWidget(self.scrollarea2)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem10)
        self.lb_amount = QtWidgets.QLabel(self.tab)
        self.lb_amount.setObjectName("lb_amount")
        self.horizontalLayout_6.addWidget(self.lb_amount)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.bt_done = QtWidgets.QPushButton(self.tab)
        self.bt_done.setObjectName("bt_done")
        self.horizontalLayout_6.addWidget(self.bt_done)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 5)
        self.horizontalLayout_6.setStretch(2, 1)
        self.horizontalLayout_6.setStretch(3, 4)
        self.horizontalLayout_6.setStretch(4, 15)
        self.horizontalLayout_6.setStretch(5, 10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 30)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 4)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem12)
        self.bt_refresh_status = QtWidgets.QPushButton(self.tab_2)
        self.bt_refresh_status.setObjectName("bt_refresh_status")
        self.horizontalLayout_7.addWidget(self.bt_refresh_status)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.tb_status = QtWidgets.QTextBrowser(self.tab_2)
        self.tb_status.setObjectName("tb_status")
        self.verticalLayout_2.addWidget(self.tb_status)
        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(1, 30)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem13)
        self.bt_refresh_bill = QtWidgets.QPushButton(self.tab_3)
        self.bt_refresh_bill.setObjectName("bt_refresh_bill")
        self.horizontalLayout_9.addWidget(self.bt_refresh_bill)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.tb_bill = QtWidgets.QTextBrowser(self.tab_3)
        self.tb_bill.setObjectName("tb_bill")
        self.verticalLayout_4.addWidget(self.tb_bill)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem14)
        self.bt_checkout = QtWidgets.QPushButton(self.tab_3)
        self.bt_checkout.setObjectName("bt_checkout")
        self.horizontalLayout_8.addWidget(self.bt_checkout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.verticalLayout_4.setStretch(0, 4)
        self.verticalLayout_4.setStretch(1, 30)
        self.verticalLayout_4.setStretch(2, 4)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.rbt_veg.setText(_translate("Form", "Only Veg"))
        self.gp_region.setTitle(_translate("Form", "Region"))
        self.rbt_rajas.setText(_translate("Form", "Rajasthani"))
        self.rbt_thai.setText(_translate("Form", "Thai"))
        self.rbt_north_ind.setText(_translate("Form", "North Indian"))
        self.rbt_china.setText(_translate("Form", "Chinese"))
        self.rbt_italian.setText(_translate("Form", "Italian"))
        self.rbt_south_ind.setText(_translate("Form", "South Indian"))
        self.rbt_conti.setText(_translate("Form", "Continental"))
        self.rbt_none.setText(_translate("Form", "None"))
        self.gp_type.setTitle(_translate("Form", "Type"))
        self.rbt_main.setText(_translate("Form", "Main Course"))
        self.rbt_refresh.setText(_translate("Form", "Refreshments"))
        self.rbt_dessert.setText(_translate("Form", "Dessert"))
        self.rbt_starter.setText(_translate("Form", "Starter"))
        self.rbt_bread.setText(_translate("Form", "Bread"))
        self.bt_get.setText(_translate("Form", "Get"))
        self.label.setText(_translate("Form", "Total Amount :"))
        self.lb_amount.setText(_translate("Form", "0"))
        self.bt_done.setText(_translate("Form", "Done"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Order Now"))
        self.bt_refresh_status.setText(_translate("Form", "Refresh"))
        self.tb_status.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      </p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Status"))
        self.bt_refresh_bill.setText(_translate("Form", "Refresh"))
        self.tb_bill.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.bt_checkout.setText(_translate("Form", "Checkout"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Bill"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
