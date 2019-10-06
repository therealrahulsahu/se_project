def run_main_order_now(curr_wid, MW):
    from PyQt5.QtWidgets import QHBoxLayout

    food_list = []

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

