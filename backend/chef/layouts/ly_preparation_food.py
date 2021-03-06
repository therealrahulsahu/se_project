from PyQt5.QtWidgets import QHBoxLayout


class PreparationWidget(QHBoxLayout):
    def __init__(self, cus_id, food_id, f_name, f_quantity, cus_table, parent_class):
        super().__init__()
        self.parent_class = parent_class

        self.cus_id = cus_id
        self.food_id = food_id
        self.f_name = f_name
        self.f_quantity = f_quantity
        self.cus_table = cus_table
        from PyQt5 import QtWidgets

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
        self.parent_class.th_mark_prepared.set_arg(self.cus_id, self.food_id, prepared_btn)
        self.parent_class.th_mark_prepared.start()
