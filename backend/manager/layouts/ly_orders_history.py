from PyQt5.QtWidgets import QHBoxLayout


class OrdersHistoryWidget(QHBoxLayout):
    def __init__(self, order_id, name, order_no, in_time, status, parent_class):
        super().__init__()
        self.order_id = order_id
        self.parent_class = parent_class

        from PyQt5 import QtWidgets
        if status:
            message = 'Paid'
        else:
            message = 'Dining...'

        lb_name = QtWidgets.QLabel(name)
        self.addWidget(lb_name)
        lb_order_no = QtWidgets.QLabel(str(order_no))
        self.addWidget(lb_order_no)
        lb_time = QtWidgets.QLabel(in_time.strftime('%c'))
        self.addWidget(lb_time)
        lb_status = QtWidgets.QLabel(message)
        self.addWidget(lb_status)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacerItem1)
        bt_bill = QtWidgets.QPushButton('Fetch Bill')
        self.addWidget(bt_bill)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacerItem2)
        self.setStretch(0, 1)
        self.setStretch(1, 1)
        self.setStretch(2, 2)
        self.setStretch(3, 1)
        self.setStretch(4, 1)
        self.setStretch(5, 1)
        self.setStretch(6, 1)

        bt_bill.clicked.connect(self.fetch_bill_func)
        self.parent_class.th_bill_fetch.signal.connect(self.finish_fetch_bill_func)

    def fetch_bill_func(self):
        btn = self.sender()
        self.parent_class.th_bill_fetch.set_arg(btn, self.order_id)
        self.parent_class.MW.mess('Fetching Bill...')
        btn.setEnabled(False)
        self.parent_class.th_bill_fetch.start()

    def finish_fetch_bill_func(self):
        self.parent_class.MW.mess('Bill Fetched')
        from backend import CommonFunctions
        self.parent_class.di_bill.set_n_run(
            CommonFunctions().convert_to_bill(self.parent_class.th_bill_fetch.bill_doc,
                                              self.parent_class.th_bill_fetch.fetch_dict))
