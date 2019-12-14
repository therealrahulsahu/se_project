class RunMainChangeFoodAva:
    def __init__(self, curr_wid, MW):

        self.curr_wid = curr_wid
        self.MW = MW

        from backend.chef.threads.change_food_ava import ThreadGetFoodList, ThreadMarkAva, ThreadMarkUnAva
        self.th_get_food_list = ThreadGetFoodList(self)
        self.th_mark_ava = ThreadMarkAva(self)
        self.th_mark_un_ava = ThreadMarkUnAva(self)

        self.curr_wid.bt_mark_ava.setEnabled(False)
        self.curr_wid.bt_mark_un_ava.setEnabled(False)

        self.curr_wid.bt_get_food.clicked.connect(self.get_food_thread)
        self.th_get_food_list.signal.connect(self.finish_get_food_thread)

        self.curr_wid.bt_mark_ava.clicked.connect(self.mark_food_ava)
        self.th_mark_ava.signal.connect(self.finish_mark_food_ava)
        self.th_mark_un_ava.signal.connect(self.finish_mark_food_ava)

        self.curr_wid.bt_mark_un_ava.clicked.connect(self.mark_food_un_ava)

    def get_food_thread(self):
        self.MW.mess('Fetching List...')
        self.curr_wid.bt_get_food.setEnabled(False)
        self.th_get_food_list.start()

    def finish_get_food_thread(self):
        to_be_add = ['{}{}{}'.format(x['name'], ' ' * 10, bool(x['available']))
                     for x in self.th_get_food_list.output]
        self.curr_wid.cb_food_list.addItems(to_be_add)
        self.MW.mess('Food Fetched')
        self.curr_wid.bt_mark_ava.setEnabled(True)
        self.curr_wid.bt_mark_un_ava.setEnabled(True)

    def mark_food_ava(self):
        self.MW.mess('Marking Unavailable')
        self.curr_wid.bt_get_food.setEnabled(False)
        self.curr_wid.bt_mark_ava.setEnabled(False)
        self.curr_wid.bt_mark_un_ava.setEnabled(False)
        self.th_mark_ava.start()

    def finish_mark_food_ava(self):
        self.curr_wid.cb_food_list.clear()

    def mark_food_un_ava(self):
        self.MW.mess('Mark Available')
        self.curr_wid.bt_get_food.setEnabled(False)
        self.curr_wid.bt_mark_ava.setEnabled(False)
        self.curr_wid.bt_mark_un_ava.setEnabled(False)
        self.th_mark_un_ava.start()
