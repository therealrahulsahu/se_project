from PyQt5.QtWidgets import QHBoxLayout


class StatusMenuWidget(QHBoxLayout):
    def __init__(self, f_id, f_name, f_quantity, f_p_ing, f_p_ed, parent_class):
        super().__init__()

        self.f_id = f_id
        self.rm_quantity = 0
        self.parent_class = parent_class

        from PyQt5 import QtWidgets, QtCore

        lb_name = QtWidgets.QLabel(f_name)
        self.addWidget(lb_name)
        lb_quantity = QtWidgets.QLabel(str(f_quantity))
        self.addWidget(lb_quantity)
        lb_p_ing = QtWidgets.QLabel(str(f_p_ing))
        self.addWidget(lb_p_ing)
        lb_p_ed = QtWidgets.QLabel(str(f_p_ed))
        self.addWidget(lb_p_ed)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
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
            from backend.dialogs import DialogConfirmation
            message_box = DialogConfirmation('Remove ' + str(self.rm_quantity) + ' Items ?')
            if message_box.exec_() == message_box.Yes:
                remove_btn = self.sender()
                self.parent_class.th_remove.set_arg(self.f_id, self.rm_quantity, remove_btn)
                remove_btn.setEnabled(False)
                self.parent_class.MW.mess('Removing...')
                self.parent_class.th_remove.start()
            else:
                self.parent_class.MW.mess('Cancelled')
        else:
            self.parent_class.MW.mess('Quantity is Zero')

    def change_quantity(self):
        sender_obj = self.sender()
        try:
            val = int(sender_obj.text().strip())
            if 0 < val < 50:
                self.rm_quantity = val
                self.parent_class.MW.mess('Quantity Changed')
            else:
                raise ValueError
        except ValueError:
            self.parent_class.MW.mess('Invalid Quantity')
            self.rm_quantity = 0
            sender_obj.setText('0')
