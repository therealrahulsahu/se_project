class RunMainOrderNow:
    def __init__(self, curr_wid, MW):
        self.searched_food_list = []
        self.selected_food_list = []
        self.curr_wid = curr_wid
        self.MW = MW

        from backend.threads import ThreadFetchImage, ThreadGetMenu, ThreadDoneDining
        self.th_fetch_image = ThreadFetchImage(self)
        self.th_get_menu = ThreadGetMenu(self)
        self.th_done_thread = ThreadDoneDining(self)

        self.curr_wid.bt_get.clicked.connect(self.get_menu_func)
        self.th_get_menu.signal.connect(self.finish_menu_func)

        self.curr_wid.bt_done.clicked.connect(self.done_func)
        self.th_done_thread.signal.connect(self.finish_done_func)
        self.th_done_thread.fail_signal.connect(self.fail_finish_done_func)

        from PyQt5.QtWidgets import QDialog
        from PyQt5.QtCore import Qt
        self.dialog_img = QDialog(MW, Qt.WindowCloseButtonHint)

        from PyQt5.QtWidgets import QVBoxLayout
        self.vertical_box = QVBoxLayout()
        self.dialog_img.setLayout(self.vertical_box)

        from images import ic_milkshake
        self.dialog_img.setWindowIcon(ic_milkshake)

    def get_menu_func(self):
        self.searched_food_list.clear()
        self.curr_wid.bt_get.setEnabled(False)
        from backend import CommonFunctions
        cl = CommonFunctions()
        cl.clear_layout(self.curr_wid.scroll_choose)
        self.MW.mess('Fetching Menu...')
        self.th_get_menu.start()

    def finish_menu_func(self):
        self.MW.mess('Food Fetched')

        from backend.Layouts import AddMenuWidget
        for x in self.searched_food_list:
            self.curr_wid.scroll_choose.addLayout(AddMenuWidget(x['name'], str(x['price']),
                                                                x['_id'], self))

    def done_func(self):
        if not self.selected_food_list:
            self.MW.mess('No Food Selected')
        else:
            from backend.dialogs import DialogConfirmation
            message_box = DialogConfirmation('Proceed ?')
            if message_box.exec_() == message_box.Yes:
                self.curr_wid.bt_done.setEnabled(False)
                self.th_done_thread.start()
            else:
                self.MW.mess('Cancelled')

    def finish_done_func(self):
        self.MW.mess('Order Placed')
        from backend import CommonFunctions
        cl = CommonFunctions()
        cl.clear_layout(self.curr_wid.scroll_choose)
        cl.clear_layout(self.curr_wid.scroll_select)
        self.selected_food_list.clear()
        self.searched_food_list.clear()
        self.curr_wid.lb_amount.setText('0')
        self.curr_wid.rbt_north_ind.setChecked(True)
        self.curr_wid.rbt_starter.setChecked(True)
        self.curr_wid.rbt_veg.setChecked(False)

        self.curr_wid.bt_done.setEnabled(True)

    def fail_finish_done_func(self):
        self.curr_wid.bt_done.setEnabled(True)

    def finish_open_image(self):
        from backend import CommonFunctions
        cl = CommonFunctions()
        cl.clear_layout(self.vertical_box)

        self.MW.mess('Image Retrieved')
        from os.path import expanduser, join
        from os import mkdir
        try:
            mkdir(join(expanduser('~'), 'Documents', 'Cyber_Temp'))
        except FileExistsError:
            pass
        try:
            mkdir(join(expanduser('~'), 'Documents', 'Cyber_Temp', 'Photos'))
        except FileExistsError:
            pass

        file_path = join(expanduser('~'), 'Documents', 'Cyber_Temp', 'Photos',
                         str(self.th_fetch_image.ob_id) + '.jpg')

        with open(file_path, 'wb') as save_file:
            save_file.write(self.th_fetch_image.output)  # Adding Image

        from PyQt5.QtGui import QPixmap
        pix = QPixmap(file_path)

        from PyQt5.QtWidgets import QLabel
        self.dialog_img.setWindowTitle(self.th_fetch_image.food_name)

        lb_img = QLabel()
        self.vertical_box.addWidget(lb_img)

        lb_img.setPixmap(pix)

        width_img = pix.width()
        height_img = pix.height()

        lb_img.setPixmap(pix.scaled(width_img, height_img))
        self.dialog_img.resize(width_img, height_img)
        self.dialog_img.show()
