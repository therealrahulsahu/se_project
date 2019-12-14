from PyQt5.QtWidgets import QHBoxLayout


class AddMenuWidget(QHBoxLayout):
    def __init__(self, food_name, food_price, DB_id, parent_class):
        super().__init__()
        self.DB_id = DB_id
        self.food_name = food_name
        self.food_price = food_price
        self.parent_class = parent_class

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
        bt_show_image.clicked.connect(self.open_image)
        self.parent_class.th_fetch_image.signal.connect(self.parent_class.finish_open_image)

    def open_image(self):
        btn = self.sender()
        self.parent_class.MW.mess('Retrieving Image...')
        self.parent_class.th_fetch_image.set_arg(btn, self.DB_id, self.food_name)
        from os.path import expanduser, join
        try:
            file_path = join(expanduser('~'), 'Documents', 'Cyber_Temp', 'Photos', str(self.DB_id) + '.jpg')
            with open(file_path, 'rb') as save_file:
                self.parent_class.th_fetch_image.output = save_file.read()  # Adding Image
            self.parent_class.finish_open_image()
        except FileNotFoundError:
            btn.setEnabled(False)
            self.parent_class.th_fetch_image.start()

    def to_selected(self):
        execute = True
        for x in self.parent_class.selected_food_list:
            if x.DB_id == self.DB_id:
                execute = False
        if execute:
            from backend.customer.layouts import SelectedMenuWidget
            ob = SelectedMenuWidget(self.food_name, self.food_price, self.DB_id, self.parent_class)
            self.parent_class.selected_food_list.append(ob)
            self.parent_class.curr_wid.scroll_select.addLayout(ob)
            self.update_amount()
            self.parent_class.MW.mess('Food Added')
        else:
            self.parent_class.MW.mess('Food Already Added')

    def update_amount(self):
        amount = 0
        for x in self.parent_class.selected_food_list:
            amount += x.food_price * x.quantity
        self.parent_class.curr_wid.lb_amount.setText(str(amount))
