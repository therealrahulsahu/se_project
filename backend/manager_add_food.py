def run_main_add_food(curr_wid, MW):
    def get_food_id():
        myc = MW.DB.counter
        food_id = myc.find_one({'type': 'food'})['num']
        return int(food_id)

    def update_food(in_name, in_region, in_type, in_veg, in_price, food_id):
        myc = MW.DB.food
        data = {
            'fid': food_id,
            'name': in_name,
            'region': in_region,
            'type': in_type,
            'veg': in_veg,
            'price': in_price,
            'available': True,
        }
        ret_id = myc.insert_one(data)

    def check_food_availability(in_name):
        from errors import FoodAlreadyAvailableError
        myc = MW.DB.food
        ret_data = myc.find_one({'name': in_name})
        if bool(ret_data):
            raise FoodAlreadyAvailableError

    def revert_entry_done(in_id):
        myc = MW.DB.food
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.delete_one({'fid': in_id})
        except AutoReconnect:
            revert_entry_done(in_id)

    def update_food_counter(in_id):
        myc = MW.DB.counter
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.update_one({'type': 'food'}, {'$set': {'num': in_id}})
        except AutoReconnect:
            revert_entry_done(in_id)

    from PyQt5.QtCore import QThread, pyqtSignal

    class ThreadAddFood(QThread):

        def __init__(self):
            super().__init__()

        def set_arg(self, data):
            self.data = data

        def run(self):

            from errors import FoodAlreadyAvailableError
            from pymongo.errors import AutoReconnect
            try:
                food_id = get_food_id() + 1
                check_food_availability(self.data[0])
                update_food(*self.data, food_id)
                update_food_counter(int(food_id))

                MW.mess('Food Entry Done')

            except FoodAlreadyAvailableError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_add_food.setEnabled(True)

    class ThreadGetList(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.output_list = []

        def run(self):
            in_name = r'(?i){}'.format(curr_wid.le_name_query.text().strip())
            self.output_list = []
            from errors import FoodNotFoundError
            from pymongo.errors import AutoReconnect
            try:
                myc = MW.DB.food
                data_list = list(myc.find({'name': {'$regex': in_name}},
                                          {'fid': 0, 'available': 0}).limit(10))
                if data_list:
                    curr_wid.cb_rm_food.addItems(
                        ['{0:<20} {1:<5} {2:<5} {3:<5} {4:<5}'.format(x['name'], x['region'], x['type'],
                                                                      str(x['veg']), x['price']) for x in data_list])
                    self.output_list = [x['_id'] for x in data_list]
                    self.signal.emit(True)
                else:
                    raise FoodNotFoundError
            except FoodNotFoundError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get.setEnabled(True)

    class ThreadRemoveFood(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            try:
                index = curr_wid.cb_rm_food.currentIndex()
                to_be_delete_id = th_get_food_list.output_list[index]

                myc = MW.DB.food
                ret_del = myc.delete_one({'_id': to_be_delete_id})
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get.setEnabled(True)

    class ThreadUploadImage(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def set_arg(self, food_id, location):
            self.food_id = food_id
            self.location = location

        def run(self):
            from pymongo.errors import AutoReconnect
            myc = MW.DB.food
            try:
                if self.location:
                    open_file = open(self.location, 'rb')
                    im_data = open_file.read()
                    open_file.close()

                    ret_id = myc.update_one({'_id': self.food_id}, {'$set': {'food_image': im_data}})
                    MW.mess('Image Upload Successful')
                else:
                    MW.mess('Image Selection Rejected')
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')

    th_upload_image_thread = ThreadUploadImage()

    class ThreadAddImage(QThread):
        signal = pyqtSignal('PyQt_PyObject')
        signal_message = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            try:
                index = curr_wid.cb_rm_food.currentIndex()
                self.food_id = th_get_food_list.output_list[index]

                myc = MW.DB.food
                ret_tuple = myc.find_one({'_id': self.food_id}, {'food_image': 1})
                try:
                    image = ret_tuple['food_image']
                    if not bool(image):
                        raise KeyError

                    self.signal_message.emit(True)
                except KeyError:
                    self.signal.emit(True)  # Now Proceed For upload

            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get.setEnabled(True)

    class ThreadRemoveImage(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            try:
                index = curr_wid.cb_rm_food.currentIndex()
                food_id = th_get_food_list.output_list[index]

                myc = MW.DB.food
                ret_id = myc.update_one({'_id': food_id}, {'$set': {'food_image': b''}})
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get.setEnabled(True)

    th_add_food = ThreadAddFood()
    th_get_food_list = ThreadGetList()
    th_remove_food = ThreadRemoveFood()
    th_add_img = ThreadAddImage()
    th_remove_image = ThreadRemoveImage()

    curr_wid.bt_rm_food.setEnabled(False)
    curr_wid.bt_add_img.setEnabled(False)
    curr_wid.bt_rm_img.setEnabled(False)

    def add_food_func():
        MW.mess('Adding Food')

        in_name = curr_wid.le_f_name.text().strip()
        in_region = curr_wid.le_f_region.text().strip()
        in_type = curr_wid.le_f_type.text().strip()
        in_veg = curr_wid.le_f_veg.text().strip()
        in_price = curr_wid.le_price.text().strip()
        from .reg_ex_validation import validFoodName, validRegion, validType, validBool, validPrice
        from errors import InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, \
            InvalidPriceError

        try:
            if not validFoodName(in_name):
                raise InvalidNameError
            if not validRegion(in_region):
                raise InvalidRegionError
            if not validType(in_type):
                raise InvalidTypeError
            if not validBool(in_veg):
                raise InvalidBoolError
            if not validPrice(in_price):
                raise InvalidPriceError

            if in_veg == 'True':
                in_veg = True
            else:
                in_veg = False

            message_script = ("{:<10}{:<20}\n"*5).format('Name : ', in_name,
                                                         'Region : ', in_region,
                                                         'Type : ', in_type,
                                                         'Veg : ', str(in_veg),
                                                         'Price : ', in_price)
            from .common_functions import DialogConfirmation
            message_box = DialogConfirmation(message_script)
            if message_box.exec_() == DialogConfirmation.Yes:
                th_add_food.set_arg([in_name, in_region, in_type, in_veg, int(in_price)])
                curr_wid.bt_add_food.setEnabled(False)
                th_add_food.start()
            else:
                MW.mess('Cancelled')
        except (InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, InvalidPriceError) as ob:
            MW.mess(str(ob))

    def get_food_list_func():
        MW.mess('Fetching Food List...')
        curr_wid.cb_rm_food.clear()
        curr_wid.bt_get.setEnabled(False)
        th_get_food_list.start()

    def finish_get_food_list_func():
        curr_wid.bt_rm_food.setEnabled(True)
        curr_wid.bt_add_img.setEnabled(True)
        curr_wid.bt_rm_img.setEnabled(True)
        MW.mess('Food Fetched')

    def remove_food_func():
        from .common_functions import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Remove')
        response = message_box.exec_()
        if response == message_box.Yes:
            curr_wid.bt_rm_food.setEnabled(False)
            curr_wid.bt_add_img.setEnabled(False)
            curr_wid.bt_rm_img.setEnabled(False)

            curr_wid.bt_get.setEnabled(False)
            MW.mess('Removing...')
            th_remove_food.start()
        elif response == message_box.No:
            MW.mess('Cancelled')

    def finish_remove_food_func():
        curr_wid.cb_rm_food.clear()
        MW.mess('Removed')

    def add_image_func():
        curr_wid.bt_rm_food.setEnabled(False)
        curr_wid.bt_add_img.setEnabled(False)
        curr_wid.bt_rm_img.setEnabled(False)

        curr_wid.bt_get.setEnabled(False)
        MW.mess('Adding Image...')
        th_add_img.start()

    def finish_add_image_func():
        curr_wid.cb_rm_food.clear()
        from PyQt5.QtWidgets import QFileDialog
        from os.path import expanduser
        folder = expanduser('~')
        file_dia = QFileDialog.getOpenFileName(MW, 'Select Image', folder, 'Image files (*.jpg)')
        file_location = file_dia[0]

        if file_location:
            th_upload_image_thread.set_arg(th_add_img.food_id, file_location)
            th_upload_image_thread.start()
        else:
            MW.mess('Selection Cancelled')

    def message_prompt_func():
        from .common_functions import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Replace')
        response = message_box.exec_()
        if response == message_box.Yes:
            th_add_img.signal.emit(True)
        elif response == message_box.No:
            curr_wid.cb_rm_food.clear()
            MW.mess('Image Already Available')

    def remove_image_func():
        from .common_functions import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Remove Image')
        response = message_box.exec_()
        if response == message_box.Yes:
            curr_wid.bt_rm_food.setEnabled(False)
            curr_wid.bt_add_img.setEnabled(False)
            curr_wid.bt_rm_img.setEnabled(False)

            curr_wid.bt_get.setEnabled(False)

            MW.mess('Removing Image...')
            th_remove_image.start()
        elif response == message_box.No:
            MW.mess('Cancelled')

    def finish_remove_image_func():
        curr_wid.cb_rm_food.clear()
        MW.mess('Image Removed')

    curr_wid.bt_add_food.clicked.connect(add_food_func)

    curr_wid.bt_get.clicked.connect(get_food_list_func)
    th_get_food_list.signal.connect(finish_get_food_list_func)

    curr_wid.bt_rm_food.clicked.connect(remove_food_func)
    th_remove_food.signal.connect(finish_remove_food_func)

    curr_wid.bt_add_img.clicked.connect(add_image_func)
    th_add_img.signal.connect(finish_add_image_func)
    th_add_img.signal_message.connect(message_prompt_func)

    curr_wid.bt_rm_img.clicked.connect(remove_image_func)
    th_remove_image.signal.connect(finish_remove_image_func)
