class RunMainHistory:
    def __init__(self, curr_wid, MW):
        from PyQt5.QtCore import QThread, pyqtSignal
        from PyQt5.QtWidgets import QHBoxLayout, QDialog
        from datetime import datetime
        curr_wid.time_start.setDateTime(datetime.now())
        curr_wid.time_end.setDateTime(datetime.now())

        class BillDialog(QDialog):
            def __init__(self):
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
                    MW.mess('Printing Done')
                else:
                    MW.mess('Printing Rejected')

        di_bill = BillDialog()

        class ThreadBillFetch(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()
                self.bill_doc = []

            def set_arg(self, btn, order_id):
                self.btn = btn
                self.order_id = order_id

            def run(self):
                self.bill_doc = []
                from pymongo.errors import AutoReconnect
                from errors import NoOrdersFoundError
                try:
                    myc_o = MW.DB.orders
                    myc_f = MW.DB.food
                    order_data = myc_o.find_one({'_id': self.order_id},
                                                {'name': 1, 'order_no': 1, 'phone': 1, 'mail': 1,
                                                 'table_no': 1, 'foods': 1, 'quantity': 1, 'total': 1,
                                                 'in_time': 1, 'out_time': 1})
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

        th_bill_fetch = ThreadBillFetch()

        class OrdersWidget(QHBoxLayout):
            def __init__(self, order_id, name, order_no, in_time, status):
                super().__init__()
                self.order_id = order_id

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
                th_bill_fetch.signal.connect(self.finish_fetch_bill_func)

            def fetch_bill_func(self):
                btn = self.sender()
                th_bill_fetch.set_arg(btn, self.order_id)
                MW.mess('Fetching Bill...')
                btn.setEnabled(False)
                th_bill_fetch.start()

            def finish_fetch_bill_func(self):
                MW.mess('Bill Fetched')
                from .common_functions import convert_to_bill
                di_bill.set_n_run(convert_to_bill(th_bill_fetch.bill_doc, th_bill_fetch.fetch_dict))

        class ThreadGetOrders(QThread):
            signal_get_orders = pyqtSignal('PyQt_PyObject')
            signal_total_sale = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()
                self.output = []
                self.calling_func = 0

            def run(self):
                self.output.clear()
                # Sat Jan 1 00:00:00 2000
                t_start = datetime.strptime(curr_wid.time_start.dateTime().toString(), '%a %b %d %X %Y')
                t_end = datetime.strptime(curr_wid.time_end.dateTime().toString(), '%a %b %d %X %Y')
                from pymongo.errors import AutoReconnect
                from errors import InvalidTimeEntryError, NoOrdersFoundError
                myc_o = MW.DB.orders
                try:
                    if t_end < t_start:
                        raise InvalidTimeEntryError
                    in_time_query = {'$and': [{'in_time': {'$gt': t_start}}, {'in_time': {'$lt': t_end}}],
                                     'pay_done': True}
                    if self.calling_func == 0:
                        data_fetched = myc_o.find(in_time_query,
                                                  {'_id': 1, 'in_time': 1, 'name': 1, 'order_no': 1})
                        for x in data_fetched:
                            self.output.append([x['_id'], x['name'], x['order_no'], x['in_time'], True])
                        if not self.output:
                            raise NoOrdersFoundError
                        self.signal_get_orders.emit(True)
                    else:
                        data_fetched = myc_o.find(in_time_query,
                                                  {'in_time': 1, 'name': 1, 'order_no': 1, 'total': 1})
                        count = 1
                        for x in data_fetched:
                            self.output.append([count, x['name'], x['order_no'],
                                                x['in_time'].strftime('%c'), x['total']])
                            count += 1
                        if not self.output:
                            raise NoOrdersFoundError
                        self.signal_total_sale.emit(True)
                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                except (InvalidTimeEntryError, NoOrdersFoundError) as ob:
                    MW.mess(str(ob))
                finally:
                    curr_wid.bt_get_orders.setEnabled(True)
                    curr_wid.bt_t_sale.setEnabled(True)

        th_get_orders = ThreadGetOrders()

        def get_orders_func():
            MW.mess('Fetching Orders...')
            from .common_functions import clear_layout
            clear_layout(curr_wid.scroll_history)
            curr_wid.bt_get_orders.setEnabled(False)
            curr_wid.bt_t_sale.setEnabled(False)
            th_get_orders.calling_func = 0
            th_get_orders.run()

        def finish_get_orders_func():
            MW.mess('Orders Fetched')
            for x in th_get_orders.output:
                curr_wid.scroll_history.addLayout(OrdersWidget(*x))

        def get_total_sale_func():
            curr_wid.bt_t_sale.setEnabled(False)
            curr_wid.bt_get_orders.setEnabled(False)
            from .common_functions import clear_layout
            clear_layout(curr_wid.scroll_history)
            MW.mess('Fetching...')
            th_get_orders.calling_func = 1
            th_get_orders.run()

        def finish_get_total_sale_func():
            MW.mess('Fetched')
            from .common_functions import convert_to_total_sale
            di_bill.set_n_run(convert_to_total_sale(th_get_orders.output))

        curr_wid.bt_get_orders.clicked.connect(get_orders_func)
        th_get_orders.signal_get_orders.connect(finish_get_orders_func)

        curr_wid.bt_t_sale.clicked.connect(get_total_sale_func)
        th_get_orders.signal_total_sale.connect(finish_get_total_sale_func)
