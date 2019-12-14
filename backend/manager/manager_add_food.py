class RunMainAddFood:
    def __init__(self, curr_wid, MW):

        self.curr_wid = curr_wid
        self.MW = MW

        from backend.manager.threads.add_food import ThreadUploadImage, ThreadAddFood, ThreadFetchFoodList, \
            ThreadRemoveFood, ThreadAddImage, ThreadRemoveImage
        self.th_upload_image_thread = ThreadUploadImage(self)
        self.th_add_food = ThreadAddFood(self)
        self.th_get_food_list = ThreadFetchFoodList(self)
        self.th_remove_food = ThreadRemoveFood(self)
        self.th_add_img = ThreadAddImage(self)
        self.th_remove_image = ThreadRemoveImage(self)

        self.curr_wid.bt_rm_food.setEnabled(False)
        self.curr_wid.bt_add_img.setEnabled(False)
        self.curr_wid.bt_rm_img.setEnabled(False)

        self.curr_wid.bt_add_food.clicked.connect(self.add_food_func)

        self.curr_wid.bt_get.clicked.connect(self.get_food_list_func)
        self.th_get_food_list.signal.connect(self.finish_get_food_list_func)

        self.curr_wid.bt_rm_food.clicked.connect(self.remove_food_func)
        self.th_remove_food.signal.connect(self.finish_remove_food_func)

        self.curr_wid.bt_add_img.clicked.connect(self.add_image_func)
        self.th_add_img.signal.connect(self.finish_add_image_func)
        self.th_add_img.signal_message.connect(self.message_prompt_func)

        self.curr_wid.bt_rm_img.clicked.connect(self.remove_image_func)
        self.th_remove_image.signal.connect(self.finish_remove_image_func)

    def revert_entry_done(self, in_id):
        myc = self.MW.DB.food
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.delete_one({'fid': in_id})
        except AutoReconnect:
            self.revert_entry_done(in_id)

    def add_food_func(self):
        self.MW.mess('Adding Food')

        in_name = self.curr_wid.le_f_name.text().strip()
        in_region = self.curr_wid.le_f_region.text().strip()
        in_type = self.curr_wid.le_f_type.text().strip()
        in_veg = self.curr_wid.le_f_veg.text().strip()
        in_price = self.curr_wid.le_price.text().strip()
        from backend import RegExValidation
        re_val = RegExValidation()
        from errors import InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, \
            InvalidPriceError

        try:
            if not re_val.validFoodName(in_name):
                raise InvalidNameError
            if not re_val.validRegion(in_region):
                raise InvalidRegionError
            if not re_val.validType(in_type):
                raise InvalidTypeError
            if not re_val.validBool(in_veg):
                raise InvalidBoolError
            if not re_val.validPrice(in_price):
                raise InvalidPriceError

            if in_veg == 'True':
                in_veg = True
            else:
                in_veg = False

            message_script = ("{:<10}{:<20}\n" * 5).format('Name : ', in_name,
                                                           'Region : ', in_region,
                                                           'Type : ', in_type,
                                                           'Veg : ', str(in_veg),
                                                           'Price : ', in_price)
            from backend.dialogs import DialogConfirmation
            message_box = DialogConfirmation(message_script)
            if message_box.exec_() == DialogConfirmation.Yes:
                self.th_add_food.set_arg([in_name, in_region, in_type, in_veg, int(in_price)])
                self.curr_wid.bt_add_food.setEnabled(False)
                self.th_add_food.start()
            else:
                self.MW.mess('Cancelled')
        except (InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, InvalidPriceError) as ob:
            self.MW.mess(str(ob))

    def get_food_list_func(self):
        self.MW.mess('Fetching Food List...')
        self.curr_wid.cb_rm_food.clear()
        self.curr_wid.bt_get.setEnabled(False)
        self.th_get_food_list.start()

    def finish_get_food_list_func(self):
        self.curr_wid.bt_rm_food.setEnabled(True)
        self.curr_wid.bt_add_img.setEnabled(True)
        self.curr_wid.bt_rm_img.setEnabled(True)
        self.MW.mess('Food Fetched')

    def remove_food_func(self):
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Remove')
        response = message_box.exec_()
        if response == message_box.Yes:
            self.curr_wid.bt_rm_food.setEnabled(False)
            self.curr_wid.bt_add_img.setEnabled(False)
            self.curr_wid.bt_rm_img.setEnabled(False)

            self.curr_wid.bt_get.setEnabled(False)
            self.MW.mess('Removing...')
            self.th_remove_food.start()
        elif response == message_box.No:
            self.MW.mess('Cancelled')

    def finish_remove_food_func(self):
        self.curr_wid.cb_rm_food.clear()
        self.MW.mess('Removed')

    def add_image_func(self):
        self.curr_wid.bt_rm_food.setEnabled(False)
        self.curr_wid.bt_add_img.setEnabled(False)
        self.curr_wid.bt_rm_img.setEnabled(False)

        self.curr_wid.bt_get.setEnabled(False)
        self.MW.mess('Adding Image...')
        self.th_add_img.start()

    def finish_add_image_func(self):
        self.curr_wid.cb_rm_food.clear()
        from PyQt5.QtWidgets import QFileDialog
        from os.path import expanduser
        folder = expanduser('~')
        file_dia = QFileDialog.getOpenFileName(self.MW, 'Select Image', folder, 'Image files (*.jpg)')
        file_location = file_dia[0]

        if file_location:
            self.th_upload_image_thread.set_arg(self.th_add_img.food_id, file_location)
            self.th_upload_image_thread.start()
        else:
            self.MW.mess('Selection Cancelled')

    def message_prompt_func(self):
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Replace')
        response = message_box.exec_()
        if response == message_box.Yes:
            self.th_add_img.signal.emit(True)
        elif response == message_box.No:
            self.curr_wid.cb_rm_food.clear()
            self.MW.mess('Image Already Available')

    def remove_image_func(self):
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Remove Image')
        response = message_box.exec_()
        if response == message_box.Yes:
            self.curr_wid.bt_rm_food.setEnabled(False)
            self.curr_wid.bt_add_img.setEnabled(False)
            self.curr_wid.bt_rm_img.setEnabled(False)

            self.curr_wid.bt_get.setEnabled(False)

            self.MW.mess('Removing Image...')
            self.th_remove_image.start()
        elif response == message_box.No:
            self.MW.mess('Cancelled')

    def finish_remove_image_func(self):
        self.curr_wid.cb_rm_food.clear()
        self.MW.mess('Image Removed')
