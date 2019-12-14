from PyQt5.QtWidgets import QHBoxLayout


class OnOrderStatusWidget(QHBoxLayout):
    def __init__(self, customer_id, food_name, table_no, done, total, parent_class):
        super().__init__()
        self.customer_id = customer_id
        self.parent_class = parent_class
        if done:
            status = 'Done'
        else:
            status = 'Dining'

        from PyQt5 import QtWidgets
        lb_name = QtWidgets.QLabel(food_name)
        self.addWidget(lb_name)
        lb_table_no = QtWidgets.QLabel(str(table_no))
        self.addWidget(lb_table_no)
        lb_status = QtWidgets.QLabel(status)
        self.addWidget(lb_status)
        lb_total = QtWidgets.QLabel(str(total))
        self.addWidget(lb_total)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacerItem1)
        bt_print = QtWidgets.QPushButton('Print')
        self.addWidget(bt_print)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacerItem2)
        bt_pay = QtWidgets.QPushButton('Payment Done')
        self.addWidget(bt_pay)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacerItem3)
        self.setStretch(0, 2)
        self.setStretch(1, 1)
        self.setStretch(2, 1)
        self.setStretch(3, 1)
        self.setStretch(4, 1)
        self.setStretch(5, 1)
        self.setStretch(6, 1)
        self.setStretch(7, 1)
        self.setStretch(8, 1)

        bt_print.clicked.connect(self.print_func)
        bt_pay.clicked.connect(self.payment_done_func)

    def print_func(self):
        print_btn = self.sender()
        self.parent_class.MW.mess('Fetching Bill...')
        self.parent_class.th_fetch_bill.set_arg(self.customer_id, print_btn)
        print_btn.setEnabled(False)
        self.parent_class.th_fetch_bill.start()

    def payment_done_func(self):
        payment_btn = self.sender()
        self.parent_class.MW.mess('Finishing...')
        payment_btn.setEnabled(False)
        self.parent_class.th_payment_done.set_srg(payment_btn, self.customer_id)
        self.parent_class.th_payment_done.start()
