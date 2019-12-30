def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass
    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.manager.threads.add_food import ThreadUploadImage, ThreadAddFood, ThreadFetchFoodList, \
        ThreadRemoveFood, ThreadAddImage, ThreadRemoveImage
    var.th_upload_image_thread = ThreadUploadImage(var)
    var.th_add_food = ThreadAddFood(var)
    var.th_get_food_list = ThreadFetchFoodList(var)
    var.th_remove_food = ThreadRemoveFood(var)
    var.th_add_img = ThreadAddImage(var)
    var.th_remove_image = ThreadRemoveImage(var)

    curr_wid.bt_rm_food.setEnabled(False)
    curr_wid.bt_add_img.setEnabled(False)
    curr_wid.bt_rm_img.setEnabled(False)

    def revert_entry_done(in_id):
        myc = MW.DB.food
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.delete_one({'fid': in_id})
        except AutoReconnect:
            revert_entry_done(in_id)

    def add_food_func():
        MW.mess('Adding Food')

        in_name = curr_wid.le_f_name.text().strip()
        in_region = curr_wid.le_f_region.text().strip()
        in_type = curr_wid.le_f_type.text().strip()
        in_veg = curr_wid.le_f_veg.text().strip()
        in_price = curr_wid.le_price.text().strip()
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
                var.th_add_food.set_arg([in_name, in_region, in_type, in_veg, int(in_price)])
                curr_wid.bt_add_food.setEnabled(False)
                var.th_add_food.start()
            else:
                MW.mess('Cancelled')
        except (InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, InvalidPriceError) as ob:
            MW.mess(str(ob))

    def get_food_list_func():
        MW.mess('Fetching Food List...')
        curr_wid.cb_rm_food.clear()
        curr_wid.bt_get.setEnabled(False)
        var.th_get_food_list.start()

    def finish_get_food_list_func():
        curr_wid.bt_rm_food.setEnabled(True)
        curr_wid.bt_add_img.setEnabled(True)
        curr_wid.bt_rm_img.setEnabled(True)
        MW.mess('Food Fetched')

    def remove_food_func():
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Remove')
        response = message_box.exec_()
        if response == message_box.Yes:
            curr_wid.bt_rm_food.setEnabled(False)
            curr_wid.bt_add_img.setEnabled(False)
            curr_wid.bt_rm_img.setEnabled(False)

            curr_wid.bt_get.setEnabled(False)
            MW.mess('Removing...')
            var.th_remove_food.start()
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
        var.th_add_img.start()

    def finish_add_image_func():
        curr_wid.cb_rm_food.clear()
        from PyQt5.QtWidgets import QFileDialog
        from os.path import expanduser
        folder = expanduser('~')
        file_dia = QFileDialog.getOpenFileName(MW, 'Select Image', folder, 'Image files (*.jpg)')
        file_location = file_dia[0]

        if file_location:
            var.th_upload_image_thread.set_arg(var.th_add_img.food_id, file_location)
            var.th_upload_image_thread.start()
        else:
            MW.mess('Selection Cancelled')

    def message_prompt_func():
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Replace')
        response = message_box.exec_()
        if response == message_box.Yes:
            var.th_add_img.signal.emit(True)
        elif response == message_box.No:
            curr_wid.cb_rm_food.clear()
            MW.mess('Image Already Available')

    def remove_image_func():
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want To Remove Image')
        response = message_box.exec_()
        if response == message_box.Yes:
            curr_wid.bt_rm_food.setEnabled(False)
            curr_wid.bt_add_img.setEnabled(False)
            curr_wid.bt_rm_img.setEnabled(False)

            curr_wid.bt_get.setEnabled(False)

            MW.mess('Removing Image...')
            var.th_remove_image.start()
        elif response == message_box.No:
            MW.mess('Cancelled')

    def finish_remove_image_func():
        curr_wid.cb_rm_food.clear()
        MW.mess('Image Removed')

    curr_wid.bt_add_food.clicked.connect(add_food_func)

    curr_wid.bt_get.clicked.connect(get_food_list_func)
    var.th_get_food_list.signal.connect(finish_get_food_list_func)

    curr_wid.bt_rm_food.clicked.connect(remove_food_func)
    var.th_remove_food.signal.connect(finish_remove_food_func)

    curr_wid.bt_add_img.clicked.connect(add_image_func)
    var.th_add_img.signal.connect(finish_add_image_func)
    var.th_add_img.signal_message.connect(message_prompt_func)

    curr_wid.bt_rm_img.clicked.connect(remove_image_func)
    var.th_remove_image.signal.connect(finish_remove_image_func)
