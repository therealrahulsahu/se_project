class RunMainOnOrder:
    def __init__(self, curr_wid, MW):
        from PyQt5.QtWidgets import QHBoxLayout
        from PyQt5.QtCore import QThread, pyqtSignal

        class ThreadPaymentDone(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()

            def set_srg(self, btn, customer_id):
                self.btn = btn
                self.customer_id = customer_id

            def run(self):
                from pymongo.errors import AutoReconnect
                from errors import RefreshError, CustomerNotDoneYetError
                myc_o = MW.DB.orders
                try:
                    customer_data = myc_o.find_one({'_id': self.customer_id},
                                                   {'done': 1, 'pay_done': 1, 'out_time': 1})
                    if not customer_data['done']:
                        raise CustomerNotDoneYetError
                    if customer_data['pay_done']:
                        raise RefreshError
                    from datetime import datetime
                    customer_data['pay_done'] = True
                    customer_data['out_time'] = datetime.now()
                    ret_id = myc_o.update_one({'_id': self.customer_id}, {'$set': customer_data})
                    MW.mess('Payment Done')
                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->> Network Error  <<--')
                except RefreshError as ob:
                    MW.mess(str(ob))
                    self.signal.emit(True)
                except CustomerNotDoneYetError as ob:
                    MW.mess(str(ob))
                finally:
                    self.btn.setEnabled(True)

        th_payment_done = ThreadPaymentDone()

        class ThreadFetchBill(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()
                self.bill_doc = []

            def set_arg(self, customer_id, btn):
                self.customer_id = customer_id
                self.btn = btn

            def run(self):
                self.bill_doc = []
                self.fetch_dict = dict()
                from pymongo.errors import AutoReconnect
                from errors import NoOrdersFoundError
                try:
                    myc_o = MW.DB.orders
                    myc_f = MW.DB.food
                    order_data = myc_o.find_one({'_id': self.customer_id},
                                                {'name': 1, 'order_no': 1, 'phone': 1, 'mail': 1, 'table_no': 1,
                                                 'foods': 1, 'quantity': 1, 'total': 1, 'in_time': 1, 'out_time': 1})
                    self.fetch_dict = order_data
                    order_data = list(zip(order_data['foods'], order_data['quantity']))
                    for x in order_data:
                        food_detail = myc_f.find_one({'_id': x[0]}, {'name': 1, 'price': 1})
                        self.bill_doc.append(
                            [food_detail['name'], food_detail['price'], x[1], food_detail['price'] * x[1]])
                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                except NoOrdersFoundError as ob:
                    MW.mess(str(ob))
                finally:
                    self.btn.setEnabled(True)

        th_fetch_bill = ThreadFetchBill()

        class StatusWidget(QHBoxLayout):
            def __init__(self, customer_id, food_name, table_no, done, total):
                super().__init__()
                self.customer_id = customer_id
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
                MW.mess('Fetching Bill...')
                th_fetch_bill.set_arg(self.customer_id, print_btn)
                print_btn.setEnabled(False)
                th_fetch_bill.start()

            def payment_done_func(self):
                payment_btn = self.sender()
                MW.mess('Finishing...')
                payment_btn.setEnabled(False)
                th_payment_done.set_srg(payment_btn, self.customer_id)
                th_payment_done.start()

        class ThreadRefreshStatus(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()
                self.output_list = []

            def run(self):
                self.output_list.clear()
                from pymongo.errors import AutoReconnect
                from errors import CustomerNotDoneYetError
                myc_o = MW.DB.orders
                try:
                    customers_data = myc_o.find({'pay_done': False},
                                                {'_id': 1, 'name': 1, 'table_no': 1, 'done': 1, 'total': 1})
                    for x in customers_data:
                        self.output_list.append([x['_id'], x['name'], x['table_no'], x['done'], x['total']])
                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                except CustomerNotDoneYetError as ob:
                    MW.mess(str(ob))
                finally:
                    curr_wid.bt_refresh_on_order.setEnabled(True)

        th_refresh_status = ThreadRefreshStatus()

        def refresh_status_func():
            curr_wid.bt_refresh_on_order.setEnabled(False)
            from .common_functions import clear_layout
            clear_layout(curr_wid.scroll_on_order)
            MW.mess('Refreshing...')
            th_refresh_status.start()

        def finish_refresh_status_func():
            for x in th_refresh_status.output_list:
                curr_wid.scroll_on_order.addLayout(StatusWidget(*x))
            MW.mess('Refreshed')

        def printing_bill():
            from .common_functions import convert_to_bill
            data_to_print = convert_to_bill(th_fetch_bill.bill_doc, th_fetch_bill.fetch_dict)

            from PyQt5.QtPrintSupport import QPrintDialog
            dialog = QPrintDialog()

            from PyQt5.QtGui import QTextDocument

            doc = QTextDocument()
            doc.setHtml(data_to_print)

            if dialog.exec_() == QPrintDialog.Accepted:
                doc.print_(dialog.printer())
                MW.mess('Printing Done')
            else:
                MW.mess('Printing Rejected')

        curr_wid.bt_refresh_on_order.clicked.connect(refresh_status_func)
        th_refresh_status.signal.connect(finish_refresh_status_func)
        refresh_status_func()
        th_payment_done.signal.connect(refresh_status_func)
        th_fetch_bill.signal.connect(printing_bill)


def run_main_on_order(curr_wid, MW):
    from PyQt5.QtWidgets import QHBoxLayout
    from PyQt5.QtCore import QThread, pyqtSignal

    class ThreadPaymentDone(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def set_srg(self, btn, customer_id):
            self.btn = btn
            self.customer_id = customer_id

        def run(self):
            from pymongo.errors import AutoReconnect
            from errors import RefreshError, CustomerNotDoneYetError
            myc_o = MW.DB.orders
            try:
                customer_data = myc_o.find_one({'_id': self.customer_id},
                                               {'done': 1, 'pay_done': 1, 'out_time': 1})
                if not customer_data['done']:
                    raise CustomerNotDoneYetError
                if customer_data['pay_done']:
                    raise RefreshError
                from datetime import datetime
                customer_data['pay_done'] = True
                customer_data['out_time'] = datetime.now()
                ret_id = myc_o.update_one({'_id': self.customer_id}, {'$set': customer_data})
                MW.mess('Payment Done')
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error  <<--')
            except RefreshError as ob:
                MW.mess(str(ob))
                self.signal.emit(True)
            except CustomerNotDoneYetError as ob:
                MW.mess(str(ob))
            finally:
                self.btn.setEnabled(True)

    th_payment_done = ThreadPaymentDone()

    class ThreadFetchBill(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.bill_doc = []

        def set_arg(self, customer_id, btn):
            self.customer_id = customer_id
            self.btn = btn

        def run(self):
            self.bill_doc = []
            self.fetch_dict = dict()
            from pymongo.errors import AutoReconnect
            from errors import NoOrdersFoundError
            try:
                myc_o = MW.DB.orders
                myc_f = MW.DB.food
                order_data = myc_o.find_one({'_id': self.customer_id},
                                            {'name': 1, 'order_no': 1, 'phone': 1, 'mail': 1, 'table_no': 1,
                                             'foods': 1, 'quantity': 1, 'total': 1, 'in_time': 1, 'out_time': 1})
                self.fetch_dict = order_data
                order_data = list(zip(order_data['foods'], order_data['quantity']))
                for x in order_data:
                    food_detail = myc_f.find_one({'_id': x[0]}, {'name': 1, 'price': 1})
                    self.bill_doc.append([food_detail['name'], food_detail['price'], x[1], food_detail['price'] * x[1]])
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            except NoOrdersFoundError as ob:
                MW.mess(str(ob))
            finally:
                self.btn.setEnabled(True)

    th_fetch_bill = ThreadFetchBill()

    class StatusWidget(QHBoxLayout):
        def __init__(self, customer_id, food_name, table_no, done, total):
            super().__init__()
            self.customer_id = customer_id
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
            spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.addItem(spacerItem1)
            bt_print = QtWidgets.QPushButton('Print')
            self.addWidget(bt_print)
            spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.addItem(spacerItem2)
            bt_pay = QtWidgets.QPushButton('Payment Done')
            self.addWidget(bt_pay)
            spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
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
            MW.mess('Fetching Bill...')
            th_fetch_bill.set_arg(self.customer_id, print_btn)
            print_btn.setEnabled(False)
            th_fetch_bill.start()

        def payment_done_func(self):
            payment_btn = self.sender()
            MW.mess('Finishing...')
            payment_btn.setEnabled(False)
            th_payment_done.set_srg(payment_btn, self.customer_id)
            th_payment_done.start()

    class ThreadRefreshStatus(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.output_list = []

        def run(self):
            self.output_list.clear()
            from pymongo.errors import AutoReconnect
            from errors import CustomerNotDoneYetError
            myc_o = MW.DB.orders
            try:
                customers_data = myc_o.find({'pay_done': False},
                                            {'_id': 1, 'name': 1, 'table_no': 1, 'done': 1, 'total': 1})
                for x in customers_data:
                    self.output_list.append([x['_id'], x['name'], x['table_no'], x['done'], x['total']])
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            except CustomerNotDoneYetError as ob:
                MW.mess(str(ob))
            finally:
                curr_wid.bt_refresh_on_order.setEnabled(True)

    th_refresh_status = ThreadRefreshStatus()

    def refresh_status_func():
        curr_wid.bt_refresh_on_order.setEnabled(False)
        from .common_functions import clear_layout
        clear_layout(curr_wid.scroll_on_order)
        MW.mess('Refreshing...')
        th_refresh_status.start()

    def finish_refresh_status_func():
        for x in th_refresh_status.output_list:
            curr_wid.scroll_on_order.addLayout(StatusWidget(*x))
        MW.mess('Refreshed')

    def printing_bill():
        from .common_functions import convert_to_bill
        data_to_print = convert_to_bill(th_fetch_bill.bill_doc, th_fetch_bill.fetch_dict)

        from PyQt5.QtPrintSupport import QPrintDialog
        dialog = QPrintDialog()

        from PyQt5.QtGui import QTextDocument

        doc = QTextDocument()
        doc.setHtml(data_to_print)

        if dialog.exec_() == QPrintDialog.Accepted:
            doc.print_(dialog.printer())
            MW.mess('Printing Done')
        else:
            MW.mess('Printing Rejected')

    curr_wid.bt_refresh_on_order.clicked.connect(refresh_status_func)
    th_refresh_status.signal.connect(finish_refresh_status_func)
    refresh_status_func()
    th_payment_done.signal.connect(refresh_status_func)
    th_fetch_bill.signal.connect(printing_bill)
