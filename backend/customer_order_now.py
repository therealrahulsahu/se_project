def run_main_order_now(curr_wid, MW):
    from PyQt5.QtWidgets import QHBoxLayout
    from PyQt5.QtCore import QThread, pyqtSignal
    searched_food_list = []
    selected_food_list = []

    def update_amount():
        amount = 0
        for x in selected_food_list:
            amount += x.food_price * x.quantity
        curr_wid.lb_amount.setText(str(amount))

    class AddMenuWidget(QHBoxLayout):
        def __init__(self, food_name, food_price, DB_id):
            super().__init__()
            self.DB_id = DB_id
            self.food_name = food_name
            self.food_price = food_price

            from PyQt5 import QtWidgets
            lb_food_name = QtWidgets.QLabel(self.food_name)
            self.addWidget(lb_food_name)
            lb_price = QtWidgets.QLabel(self.food_price)
            self.addWidget(lb_price)
            bt_show_image = QtWidgets.QPushButton('Show Image')
            self.addWidget(bt_show_image)
            bt_add = QtWidgets.QPushButton('Add')
            self.addWidget(bt_add)
            self.setStretch(0, 2)
            self.setStretch(1, 2)
            self.setStretch(2, 1)
            self.setStretch(3, 2)

            bt_add.clicked.connect(self.to_selected)

        def to_selected(self):
            execute = True
            for x in selected_food_list:
                if x.DB_id == self.DB_id:
                    execute = False
            if execute:
                ob = SelectedMenuWidget(self.food_name, self.food_price, self.DB_id)
                selected_food_list.append(ob)
                curr_wid.scroll_select.addLayout(ob)
                update_amount()
                MW.mess('Food Added')
            else:
                MW.mess('Food Already Added')

    class SelectedMenuWidget(QHBoxLayout):
        def __init__(self, food_name, food_price, DB_id):
            super().__init__()
            self.DB_id = DB_id
            self.food_name = food_name
            self.food_price = int(food_price)
            self.quantity = 1
            from PyQt5 import QtWidgets, QtCore

            lb_food_name = QtWidgets.QLabel(self.food_name)
            self.addWidget(lb_food_name)
            lb_price = QtWidgets.QLabel(str(self.food_price))
            self.addWidget(lb_price)
            label = QtWidgets.QLabel('Quantity')
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
            self.addWidget(label)
            le_quantity = QtWidgets.QLineEdit(str(self.quantity))
            le_quantity.setInputMethodHints(QtCore.Qt.ImhNone)
            le_quantity.setMaxLength(2)
            self.addWidget(le_quantity)
            bt_remove = QtWidgets.QPushButton("Remove")
            self.addWidget(bt_remove)
            self.setStretch(0, 4)
            self.setStretch(1, 4)
            self.setStretch(2, 2)
            self.setStretch(3, 1)
            self.setStretch(4, 4)

            bt_remove.clicked.connect(self.remove_wid)
            le_quantity.editingFinished.connect(self.change_quantity)

        def remove_wid(self):
            selected_food_list.remove(self)
            clear_layout(self)
            update_amount()
            MW.mess('Food Remove')

        def change_quantity(self):
            sender_obj = self.sender()
            try:
                val = int(sender_obj.text().strip())
                if 0 < val < 50:
                    self.quantity = val
                    MW.mess('Quantity Changed')
                    update_amount()
                else:
                    raise ValueError
            except ValueError:
                MW.mess('Invalid Quantity')
                self.quantity = 1
                sender_obj.setText('1')

    def check_for_veg():
        return curr_wid.rbt_veg.isChecked()

    def check_for_region():
        if curr_wid.rbt_north_ind.isChecked():
            return 'nid'
        elif curr_wid.rbt_italian.isChecked():
            return 'ita'
        elif curr_wid.rbt_south_ind.isChecked():
            return 'sid'
        elif curr_wid.rbt_conti.isChecked():
            return 'conti'
        elif curr_wid.rbt_thai.isChecked():
            return 'thi'
        elif curr_wid.rbt_china.isChecked():
            return 'chi'
        elif curr_wid.rbt_rajas.isChecked():
            return 'raj'
        elif curr_wid.rbt_none.isChecked():
            return 'none'

    def check_for_type():
        if curr_wid.rbt_starter.isChecked():
            return 'sta'
        elif curr_wid.rbt_main.isChecked():
            return 'mcs'
        elif curr_wid.rbt_refresh.isChecked():
            return 'ref'
        elif curr_wid.rbt_dessert.isChecked():
            return 'des'
        elif curr_wid.rbt_bread.isChecked():
            return 'bre'

    class ThreadGetMenu(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            if check_for_veg():
                food_query = {
                    'veg': True,
                    'region': check_for_region(),
                    'type': check_for_type(),
                    'available': True
                }
            else:
                food_query = {
                    'region': check_for_region(),
                    'type': check_for_type(),
                    'available': True
                }

            myc = MW.DB.food
            from pymongo.errors import AutoReconnect
            from errors import FoodNotFoundError
            global searched_food_list
            try:
                data_list = list(myc.find(food_query, {'_id': 1, 'name': 1, 'price': 1}))
                if data_list:
                    searched_food_list = data_list
                    self.signal.emit(True)
                else:
                    raise FoodNotFoundError
            except FoodNotFoundError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get.setEnabled(True)

    th_get_menu = ThreadGetMenu()

    def clear_layout(layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    clear_layout(child.layout())

    def get_menu_func():
        global searched_food_list
        searched_food_list = []
        curr_wid.bt_get.setEnabled(False)
        clear_layout(curr_wid.scroll_choose)
        MW.mess('Fetching Menu...')
        th_get_menu.start()

    def finish_menu_func():
        global searched_food_list
        MW.mess('Food Fetched')

        for x in searched_food_list:
            curr_wid.scroll_choose.addLayout(AddMenuWidget(x['name'], str(x['price']), x['_id']))

    curr_wid.bt_get.clicked.connect(get_menu_func)
    th_get_menu.signal.connect(finish_menu_func)

    class ThreadDone(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            from errors import NoFoodSelectedError
            try:
                if not selected_food_list:
                    raise NoFoodSelectedError

                # Add Code Here

                self.signal.emit(True)
            except NoFoodSelectedError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_done.setEnabled(True)

    th_done_thread = ThreadDone()

    def done_func():
        curr_wid.bt_done.setEnabled(False)
        th_done_thread.start()

    def finish_done_func():
        MW.mess('Order Placed')
        clear_layout(curr_wid.scroll_choose)
        clear_layout(curr_wid.scroll_select)
        selected_food_list.clear()
        searched_food_list.clear()
        curr_wid.lb_amount.setText('0')
        curr_wid.rbt_north_ind.setChecked(True)
        curr_wid.rbt_starter.setChecked(True)
        curr_wid.rbt_veg.setChecked(False)

    curr_wid.bt_done.clicked.connect(done_func)
    th_done_thread.signal.connect(finish_done_func)