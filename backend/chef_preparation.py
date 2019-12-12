class RunMainChefPreparation:
    def __init__(self, curr_wid, MW):
        from PyQt5.QtCore import QThread, pyqtSignal
        from PyQt5 import QtWidgets
        from pymongo.errors import AutoReconnect
        myc_o = MW.DB.orders
        myc_f = MW.DB.food

        request_widget_list = []
        preparation_widget_list = []

        from .common_functions import clear_layout

        class ThreadTakeOrder(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()

            def set_arg(self, customer_id, food_id, btn):
                self.customer_id = customer_id
                self.food_id = food_id
                self.btn = btn

            def run(self):
                from errors import RefreshError
                try:
                    customer_tuple = myc_o.find_one({'_id': self.customer_id},
                                                    {'foods': 1, 'status_not_taken': 1, 'status_preparing': 1})
                    index = customer_tuple['foods'].index(self.food_id)
                    if customer_tuple['status_not_taken'][index]:
                        quantity = customer_tuple['status_not_taken'][index]
                        customer_tuple['status_not_taken'][index] = 0
                        customer_tuple['status_preparing'][index] += quantity
                        ret_id = myc_o.update_one({'_id': self.customer_id}, {'$set': customer_tuple})
                        MW.mess('Preparing Started')
                        self.signal.emit(True)
                    else:
                        raise RefreshError

                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                except RefreshError as ob:
                    MW.mess(str(ob))
                    self.signal.emit(True)
                finally:
                    self.btn.setEnabled(True)

        class ThreadMarkPrepared(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()

            def set_arg(self, customer_id, food_id, btn):
                self.customer_id = customer_id
                self.food_id = food_id
                self.btn = btn

            def run(self):
                from errors import RefreshError
                try:
                    customer_tuple = myc_o.find_one({'_id': self.customer_id},
                                                    {'foods': 1, 'status_prepared': 1, 'status_preparing': 1})
                    index = customer_tuple['foods'].index(self.food_id)
                    if customer_tuple['status_preparing'][index]:
                        quantity = customer_tuple['status_preparing'][index]
                        customer_tuple['status_preparing'][index] = 0
                        customer_tuple['status_prepared'][index] += quantity
                        ret_id = myc_o.update_one({'_id': self.customer_id}, {'$set': customer_tuple})
                        MW.mess('Prepared Marked')
                        self.signal.emit(True)
                    else:
                        raise RefreshError
                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                except RefreshError as ob:
                    MW.mess(str(ob))
                    self.signal.emit(True)
                finally:
                    self.btn.setEnabled(True)

        th_take_order = ThreadTakeOrder()
        th_mark_prepared = ThreadMarkPrepared()

        class RequestWidget(QtWidgets.QHBoxLayout):
            def __init__(self, cus_id, food_id, f_name, f_quantity, cus_table):
                super().__init__()

                self.cus_id = cus_id
                self.food_id = food_id
                self.f_name = f_name
                self.f_quantity = f_quantity
                self.cus_table = cus_table

                lb_name = QtWidgets.QLabel(self.f_name)
                self.addWidget(lb_name)
                lb_quantity = QtWidgets.QLabel(str(self.f_quantity))
                self.addWidget(lb_quantity)
                lb_table_no = QtWidgets.QLabel(str(self.cus_table))
                self.addWidget(lb_table_no)
                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Minimum)
                self.addItem(spacerItem1)
                bt_take = QtWidgets.QPushButton('Take Order')
                self.addWidget(bt_take)
                self.setStretch(0, 2)
                self.setStretch(1, 1)
                self.setStretch(2, 1)
                self.setStretch(3, 1)
                self.setStretch(4, 1)

                bt_take.clicked.connect(self.take_order_func)

            def take_order_func(self):
                take_btn = self.sender()
                take_btn.setEnabled(False)
                th_take_order.set_arg(self.cus_id, self.food_id, take_btn)
                th_take_order.start()

        class PreparationWidget(QtWidgets.QHBoxLayout):
            def __init__(self, cus_id, food_id, f_name, f_quantity, cus_table):
                super().__init__()

                self.cus_id = cus_id
                self.food_id = food_id
                self.f_name = f_name
                self.f_quantity = f_quantity
                self.cus_table = cus_table

                lb_name = QtWidgets.QLabel(self.f_name)
                self.addWidget(lb_name)
                lb_quantity = QtWidgets.QLabel(str(self.f_quantity))
                self.addWidget(lb_quantity)
                lb_table_no = QtWidgets.QLabel(str(self.cus_table))
                self.addWidget(lb_table_no)
                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Minimum)
                self.addItem(spacerItem1)
                bt_take = QtWidgets.QPushButton('Mark Prepared')
                self.addWidget(bt_take)
                self.setStretch(0, 2)
                self.setStretch(1, 1)
                self.setStretch(2, 1)
                self.setStretch(3, 1)
                self.setStretch(4, 1)

                bt_take.clicked.connect(self.mark_prepared)

            def mark_prepared(self):
                prepared_btn = self.sender()
                prepared_btn.setEnabled(False)
                th_mark_prepared.set_arg(self.cus_id, self.food_id, prepared_btn)
                th_mark_prepared.start()

        class ThreadPreparationRefresh(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()

            def run(self):
                from errors import NoOrdersFoundError
                try:
                    query_ret = {
                        '_id': 1,
                        'table_no': 1,
                        'foods': 1,
                        'status_not_taken': 1,
                        'status_preparing': 1
                    }
                    ret_customers = myc_o.find({'done': False}, query_ret)
                    for cus_dict in ret_customers:
                        cus_data = zip(cus_dict['foods'], cus_dict['status_not_taken'],
                                       cus_dict['status_preparing'])
                        for food_tuple in cus_data:
                            food_name = myc_f.find_one({'_id': food_tuple[0]}, {'name': 1})['name']
                            if food_tuple[1]:
                                request_widget_list.append(
                                    (cus_dict['_id'], food_tuple[0], food_name,
                                     food_tuple[1], cus_dict['table_no']))
                            if food_tuple[2]:
                                preparation_widget_list.append(
                                    (cus_dict['_id'], food_tuple[0], food_name,
                                     food_tuple[2], cus_dict['table_no']))

                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->> Network Error<<--')
                except NoOrdersFoundError as ob:
                    MW.mess(str(ob))
                finally:
                    curr_wid.bt_refresh.setEnabled(True)

        th_preparing_refresh = ThreadPreparationRefresh()

        def refresh_func():
            curr_wid.bt_refresh.setEnabled(False)
            clear_layout(curr_wid.scroll_req)
            clear_layout(curr_wid.scroll_pre)
            request_widget_list.clear()
            preparation_widget_list.clear()
            MW.mess('Refreshing...')
            th_preparing_refresh.start()

        def finish_refresh_func():
            for x in request_widget_list:
                curr_wid.scroll_req.addLayout(RequestWidget(*x))
            for x in preparation_widget_list:
                curr_wid.scroll_pre.addLayout(PreparationWidget(*x))
            MW.mess('Refreshed')

        curr_wid.bt_refresh.clicked.connect(refresh_func)
        th_preparing_refresh.signal.connect(finish_refresh_func)
        th_take_order.signal.connect(refresh_func)
        th_mark_prepared.signal.connect(refresh_func)
        refresh_func()
