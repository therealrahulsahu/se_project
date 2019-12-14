from PyQt5.QtWidgets import QHBoxLayout


class SelectedMenuWidget(QHBoxLayout):
    def __init__(self, food_name, food_price, DB_id, parent_class):
        super().__init__()
        self.DB_id = DB_id
        self.food_name = food_name
        self.food_price = int(food_price)
        self.quantity = 1
        self.parent_class = parent_class

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
        self.parent_class.selected_food_list.remove(self)
        from backend import CommonFunctions
        cl = CommonFunctions()
        cl.clear_layout(self)
        self.update_amount()
        self.parent_class.MW.mess('Food Removed')

    def change_quantity(self):
        sender_obj = self.sender()
        try:
            val = int(sender_obj.text().strip())
            if 0 < val < 50:
                self.quantity = val
                self.parent_class.MW.mess('Quantity Changed')
                self.update_amount()
            else:
                raise ValueError
        except ValueError:
            self.parent_class.MW.mess('Invalid Quantity')
            self.quantity = 1
            sender_obj.setText('1')

    def update_amount(self):
        amount = 0
        for x in self.parent_class.selected_food_list:
            amount += x.food_price * x.quantity
        self.parent_class.curr_wid.lb_amount.setText(str(amount))
