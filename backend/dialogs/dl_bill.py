from PyQt5.QtWidgets import QDialog


class BillDialog(QDialog):
    def __init__(self, history_class):
        self.history_class = history_class
        from PyQt5.QtCore import Qt
        super().__init__(None, Qt.WindowCloseButtonHint)

        from images import ic_milkshake
        self.setWindowIcon(ic_milkshake)
        self.move(10, 10)
        self.setWindowTitle('Customer Bill')
        from PyQt5 import QtWidgets
        self.resize(400, 500)
        verticalLayout = QtWidgets.QVBoxLayout(self)
        horizontalLayout = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem)
        bt_print = QtWidgets.QPushButton('Print')
        horizontalLayout.addWidget(bt_print)
        verticalLayout.addLayout(horizontalLayout)
        self.tb_bill = QtWidgets.QTextBrowser()
        verticalLayout.addWidget(self.tb_bill)
        verticalLayout.setStretch(0, 2)
        verticalLayout.setStretch(1, 20)

        bt_print.clicked.connect(self.print_func)

    def set_n_run(self, bill_html):
        self.bill_html = bill_html

        self.tb_bill.setHtml(self.bill_html)

        self.show()

    def print_func(self):
        from PyQt5.QtPrintSupport import QPrintDialog
        dialog = QPrintDialog()

        from PyQt5.QtGui import QTextDocument

        doc = QTextDocument()
        doc.setHtml(self.bill_html)

        if dialog.exec_() == QPrintDialog.Accepted:
            doc.print_(dialog.printer())
            self.history_class.MW.mess('Printing Done')
        else:
            self.history_class.MW.mess('Printing Rejected')
