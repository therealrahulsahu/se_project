def run_main_status(curr_wid, MW):
    from PyQt5.QtWidgets import QHBoxLayout
    from PyQt5.QtCore import QThread, pyqtSignal

    customer_id = MW.logged_user
    myc_o = MW.DB.orders
    myc_f = MW.DB.food

    def clear_layout(layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    clear_layout(child.layout())

    class ThreadRemove(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self,):
            super().__init__()

        def set_arg(self,  rm_id, rm_quan, remove_btn):
            self.rm_id = rm_id
            self.rm_quan = rm_quan
            self.remove_btn = remove_btn

        def run(self):
            from pymongo.errors import AutoReconnect
            from errors import CantRemoveOrderPreparingError
            try:
                return_query = {
                    'foods': 1,
                    'quantity': 1,
                    'status_not_taken': 1,
                    'status_preparing': 1,
                    'status_prepared': 1,
                    'total': 1
                }
                fetched_order = myc_o.find_one({'_id': customer_id}, return_query)

                f_price = myc_f.find_one({'_id': self.rm_id}, {'price': 1})
                f_price = f_price['price']

                ind = fetched_order['foods'].index(self.rm_id)
                if self.rm_quan < fetched_order['status_not_taken'][ind]:
                    fetched_order['quantity'][ind] -= self.rm_quan
                    fetched_order['status_not_taken'][ind] -= self.rm_quan
                    fetched_order['total'] -= self.rm_quan * f_price

                    ret_id = myc_o.update_one({'_id': customer_id}, {'$set': fetched_order})
                    MW.mess('Food Removed')
                    self.signal.emit(True)
                elif self.rm_quan == fetched_order['status_not_taken'][ind]:
                    fetched_order['foods'].pop(ind)
                    fetched_order['quantity'].pop(ind)
                    fetched_order['status_not_taken'].pop(ind)
                    fetched_order['status_preparing'].pop(ind)
                    fetched_order['status_prepared'].pop(ind)
                    fetched_order['total'] -= self.rm_quan * f_price

                    ret_id = myc_o.update_one({'_id': customer_id}, {'$set': fetched_order})
                    MW.mess('Food Removed')
                    self.signal.emit(True)
                else:
                    raise CantRemoveOrderPreparingError

            except CantRemoveOrderPreparingError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error<<--')
            finally:
                self.remove_btn.setEnabled(True)

    th_remove = ThreadRemove()

    class StatusMenuWidget(QHBoxLayout):
        def __init__(self, f_id, f_name, f_quantity, f_p_ing, f_p_ed):
            super().__init__()

            self.f_id = f_id
            self.rm_quantity = 0

            from PyQt5 import QtWidgets, QtCore

            lb_name = QtWidgets.QLabel(f_name)
            self.addWidget(lb_name)
            lb_quantity = QtWidgets.QLabel(str(f_quantity))
            self.addWidget(lb_quantity)
            lb_p_ing = QtWidgets.QLabel(str(f_p_ing))
            self.addWidget(lb_p_ing)
            lb_p_ed = QtWidgets.QLabel(str(f_p_ed))
            self.addWidget(lb_p_ed)
            spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.addItem(spacerItem1)
            bt_remove = QtWidgets.QPushButton('Remove')
            self.addWidget(bt_remove)
            label = QtWidgets.QLabel('Quantity : ')
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
            self.addWidget(label)
            le_quantity = QtWidgets.QLineEdit(str(self.rm_quantity))
            le_quantity.setInputMethodHints(QtCore.Qt.ImhNone)
            le_quantity.setMaxLength(2)
            self.addWidget(le_quantity)
            self.setStretch(0, 5)
            self.setStretch(1, 5)
            self.setStretch(2, 5)
            self.setStretch(3, 5)
            self.setStretch(4, 10)
            self.setStretch(5, 5)
            self.setStretch(6, 4)
            self.setStretch(7, 2)

            le_quantity.editingFinished.connect(self.change_quantity)
            bt_remove.clicked.connect(self.remove_food)

        def remove_food(self):
            if self.rm_quantity:
                remove_btn = self.sender()
                th_remove.set_arg(self.f_id, self.rm_quantity, remove_btn)
                remove_btn.setEnabled(False)
                MW.mess('Removing...')
                th_remove.start()

            else:
                MW.mess('Quantity is Zero')

        def change_quantity(self):
            sender_obj = self.sender()
            try:
                val = int(sender_obj.text().strip())
                if 0 < val < 50:
                    self.rm_quantity = val
                    MW.mess('Quantity Changed')
                else:
                    raise ValueError
            except ValueError:
                MW.mess('Invalid Quantity')
                self.rm_quantity = 0
                sender_obj.setText('0')

    new_list = []

    class ThreadRefresh(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            myc = MW.DB.orders
            try:
                return_query = {
                    'foods': 1,
                    'quantity': 1,
                    'status_preparing': 1,
                    'status_prepared': 1
                }
                order_set = myc.find_one({'_id': customer_id}, return_query)

                order_set = list(zip(order_set['foods'], order_set['quantity'],
                                     order_set['status_preparing'], order_set['status_prepared']))

                myc = MW.DB.food
                for x in order_set:
                    ret_name = myc.find_one({'_id': x[0]}, {'name': 1})
                    new_list.append([x[0], ret_name['name'], x[1], x[2], x[3]])
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_refresh_status.setEnabled(True)

    th_refresh = ThreadRefresh()

    def refresh_func():
        new_list.clear()
        curr_wid.bt_refresh_status.setEnabled(False)
        th_refresh.start()
        MW.mess('Refreshing...')

    def finish_refresh_func():
        clear_layout(curr_wid.scroll_status)
        if new_list:
            for x in new_list:
                curr_wid.scroll_status.addLayout(StatusMenuWidget(x[0], x[1], x[2], x[3], x[4]))
            MW.mess('Refreshed')
        else:
            MW.mess('No Orders Found')

    curr_wid.bt_refresh_status.clicked.connect(refresh_func)
    th_refresh.signal.connect(finish_refresh_func)
    th_remove.signal.connect(refresh_func)
    # refresh_func()
