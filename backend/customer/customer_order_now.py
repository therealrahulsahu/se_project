def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass

    var = Variables()
    var.searched_food_list = []
    var.selected_food_list = []
    var.curr_wid = curr_wid
    var.MW = MW

    from PyQt5.QtWidgets import QDialog
    from PyQt5.QtCore import Qt
    dialog_img = QDialog(MW, Qt.WindowCloseButtonHint)

    from PyQt5.QtWidgets import QVBoxLayout
    vertical_box = QVBoxLayout()
    dialog_img.setLayout(vertical_box)

    from images import ic_milkshake
    dialog_img.setWindowIcon(ic_milkshake)

    from backend.customer.threads.order_now import ThreadFetchImage, ThreadGetMenu, ThreadDoneDining
    var.th_fetch_image = ThreadFetchImage(var)
    var.th_get_menu = ThreadGetMenu(var)
    var.th_done_thread = ThreadDoneDining(var)

    def get_menu_func():
        var.searched_food_list.clear()
        curr_wid.bt_get.setEnabled(False)
        from backend import CommonFunctions
        cl = CommonFunctions()
        cl.clear_layout(curr_wid.scroll_choose)
        MW.mess('Fetching Menu...')
        var.th_get_menu.start()

    def finish_menu_func():
        MW.mess('Food Fetched')

        from backend.customer.layouts import AddMenuWidget
        for x in var.searched_food_list:
            curr_wid.scroll_choose.addLayout(AddMenuWidget(x['name'], str(x['price']),
                                                                x['_id'], var))

    def done_func():
        if not var.selected_food_list:
            MW.mess('No Food Selected')
        else:
            from backend.dialogs import DialogConfirmation
            message_box = DialogConfirmation('Proceed ?')
            if message_box.exec_() == message_box.Yes:
                curr_wid.bt_done.setEnabled(False)
                var.th_done_thread.start()
            else:
                MW.mess('Cancelled')

    def finish_done_func():
        MW.mess('Order Placed')
        from backend import CommonFunctions
        cl = CommonFunctions()
        cl.clear_layout(curr_wid.scroll_choose)
        cl.clear_layout(curr_wid.scroll_select)
        var.selected_food_list.clear()
        var.searched_food_list.clear()
        curr_wid.lb_amount.setText('0')
        curr_wid.rbt_north_ind.setChecked(True)
        curr_wid.rbt_starter.setChecked(True)
        curr_wid.rbt_veg.setChecked(False)

        curr_wid.bt_done.setEnabled(True)

    def fail_finish_done_func():
        curr_wid.bt_done.setEnabled(True)

    def finish_open_image():
        from backend import CommonFunctions
        cl = CommonFunctions()
        cl.clear_layout(vertical_box)

        MW.mess('Image Retrieved')
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
                         str(var.th_fetch_image.ob_id) + '.jpg')

        with open(file_path, 'wb') as save_file:
            save_file.write(var.th_fetch_image.output)  # Adding Image

        from PyQt5.QtGui import QPixmap
        pix = QPixmap(file_path)

        from PyQt5.QtWidgets import QLabel
        dialog_img.setWindowTitle(var.th_fetch_image.food_name)

        lb_img = QLabel()
        vertical_box.addWidget(lb_img)

        lb_img.setPixmap(pix)

        width_img = pix.width()
        height_img = pix.height()

        lb_img.setPixmap(pix.scaled(width_img, height_img))
        dialog_img.resize(width_img, height_img)
        dialog_img.show()

    curr_wid.bt_get.clicked.connect(get_menu_func)
    var.th_get_menu.signal.connect(finish_menu_func)

    curr_wid.bt_done.clicked.connect(done_func)
    var.th_done_thread.signal.connect(finish_done_func)
    var.th_done_thread.fail_signal.connect(fail_finish_done_func)
    var.finish_open_image = finish_open_image