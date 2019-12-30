def run_main(curr_wid, MW):

    class Variables:
        def __init__(self):
            pass
    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.chef.threads.change_food_ava import ThreadGetFoodList, ThreadMarkAva, ThreadMarkUnAva
    var.th_get_food_list = ThreadGetFoodList(var)
    var.th_mark_ava = ThreadMarkAva(var)
    var.th_mark_un_ava = ThreadMarkUnAva(var)

    curr_wid.bt_mark_ava.setEnabled(False)
    curr_wid.bt_mark_un_ava.setEnabled(False)

    def get_food_thread():
        MW.mess('Fetching List...')
        curr_wid.cb_food_list.clear()
        curr_wid.bt_get_food.setEnabled(False)
        var.th_get_food_list.start()

    def finish_get_food_thread():
        to_be_add = ['{}{}{}'.format(x['name'], ' ' * 10, bool(x['available']))
                     for x in var.th_get_food_list.output]
        curr_wid.cb_food_list.addItems(to_be_add)
        MW.mess('Food Fetched')
        curr_wid.bt_mark_ava.setEnabled(True)
        curr_wid.bt_mark_un_ava.setEnabled(True)

    def mark_food_ava():
        MW.mess('Marking Unavailable')
        curr_wid.bt_get_food.setEnabled(False)
        curr_wid.bt_mark_ava.setEnabled(False)
        curr_wid.bt_mark_un_ava.setEnabled(False)
        var.th_mark_ava.start()

    def finish_mark_food_ava():
        curr_wid.cb_food_list.clear()

    def mark_food_un_ava():
        MW.mess('Mark Available')
        curr_wid.bt_get_food.setEnabled(False)
        curr_wid.bt_mark_ava.setEnabled(False)
        curr_wid.bt_mark_un_ava.setEnabled(False)
        var.th_mark_un_ava.start()

    curr_wid.bt_get_food.clicked.connect(get_food_thread)
    var.th_get_food_list.signal.connect(finish_get_food_thread)

    curr_wid.bt_mark_ava.clicked.connect(mark_food_ava)
    var.th_mark_ava.signal.connect(finish_mark_food_ava)
    var.th_mark_un_ava.signal.connect(finish_mark_food_ava)

    curr_wid.bt_mark_un_ava.clicked.connect(mark_food_un_ava)