def run_main_order_now(curr_wid, MW):
    from PyQt5.QtWidgets import QHBoxLayout
    from PyQt5.QtCore import QThread, pyqtSignal
    searched_food_list = []

    class AddMenuWidget(QHBoxLayout):
        def __init__(self, food_name, food_price, DB_id):
            super().__init__()
            self.DB_id = DB_id

            from PyQt5 import QtWidgets
            lb_food_name = QtWidgets.QLabel(food_name)
            self.addWidget(lb_food_name)
            lb_price = QtWidgets.QLabel(food_price)
            self.addWidget(lb_price)
            bt_show_image = QtWidgets.QPushButton('Show Image')
            self.addWidget(bt_show_image)
            bt_add = QtWidgets.QPushButton('Add')
            self.addWidget(bt_add)
            self.setStretch(0, 2)
            self.setStretch(1, 2)
            self.setStretch(2, 1)
            self.setStretch(3, 2)

    class SelectedMenuWidget(QHBoxLayout):
        def __init__(self, food_name, price, DB_id):
            super().__init__()
            self.DB_id = DB_id
            from PyQt5 import QtWidgets, QtCore

            lb_food_name = QtWidgets.QLabel(food_name)
            self.addWidget(lb_food_name)
            lb_price = QtWidgets.QLabel(price)
            self.addWidget(lb_price)
            label = QtWidgets.QLabel('Quantity')
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
            self.addWidget(label)
            self.le_quantity = QtWidgets.QLineEdit('1')
            self.le_quantity.setInputMethodHints(QtCore.Qt.ImhNone)
            self.le_quantity.setMaxLength(2)
            self.addWidget(self.le_quantity)
            self.bt_remove = QtWidgets.QPushButton("Remove")
            self.addWidget(self.bt_remove)
            self.setStretch(0, 4)
            self.setStretch(1, 4)
            self.setStretch(2, 2)
            self.setStretch(3, 1)
            self.setStretch(4, 4)

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

        # To be Removed......
        for x in searched_food_list:
            curr_wid.scroll_choose.addLayout(AddMenuWidget(x['name'], str(x['price']), x['_id']))

    curr_wid.bt_get.clicked.connect(get_menu_func)
    th_get_menu.signal.connect(finish_menu_func)