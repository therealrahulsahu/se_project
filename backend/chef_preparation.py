def run_main_chef_preparation(curr_wid, MW):
    from PyQt5.QtCore import QThread, pyqtSignal
    from PyQt5 import QtWidgets
    from pymongo.errors import AutoReconnect
    check_var = 0

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
            spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.addItem(spacerItem1)
            bt_take = QtWidgets.QPushButton('Take Order')
            self.addWidget(bt_take)
            self.setStretch(0, 1)
            self.setStretch(1, 1)
            self.setStretch(2, 1)
            self.setStretch(3, 1)
            self.setStretch(4, 1)

            bt_take.clicked.connect(self.take_order_func)

        def take_order_func(self):
            take_btn = self.sender()

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
            spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.addItem(spacerItem1)
            bt_take = QtWidgets.QPushButton('Mark Prepared')
            self.addWidget(bt_take)
            self.setStretch(0, 1)
            self.setStretch(1, 1)
            self.setStretch(2, 1)
            self.setStretch(3, 1)
            self.setStretch(4, 1)

            bt_take.clicked.connect(self.mark_prepared)

        def mark_prepared(self):
            prepared_btn = self.sender()

    class ThreadRequestRefresh(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            pass

    class ThreadPreparingRefresh(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            pass

    th_request_refresh = ThreadRequestRefresh()
    th_preparing_refresh = ThreadPreparingRefresh()

    def refresh_func():
        # curr_wid.bt_refresh.setEnabled(False)
        MW.mess('Refreshing...')
        th_request_refresh.start()
        th_preparing_refresh.start()

    # curr_wid.scroll_req.addLayout(RequestWidget('id1', 'id2', 'Paneer', 3, 6))
    # curr_wid.scroll_pre.addLayout(PreparationWidget('id1', 'id2', 'Paneer', 3, 6))
    curr_wid.bt_refresh.clicked.connect(refresh_func)
