class RunMainRestaurant:
    def __init__(self, curr_wid, MW):

        self.curr_wid = curr_wid
        self.MW = MW

        from backend.manager.threads.restau import ThreadGetTableNo, ThreadChangeTableNo
        self.th_get_table_no = ThreadGetTableNo(self)
        self.th_change_table_no = ThreadChangeTableNo(self)

        self.th_get_table_no.signal.connect(self.finish_get_table_no_func)
        self.get_table_no_func()
        self.curr_wid.le_table_no.editingFinished.connect(self.change_quantity)
        self.curr_wid.bt_change.clicked.connect(self.change_table_no_func)
        self.th_change_table_no.signal.connect(self.finish_change_table_no_func)

    def get_table_no_func(self):
        self.MW.mess('Fetching...')
        self.curr_wid.bt_change.setEnabled(False)
        self.th_get_table_no.start()

    def finish_get_table_no_func(self):
        self.MW.mess('Fetched')
        self.curr_wid.lb_table_no_2.setText(str(self.th_get_table_no.output))
        self.curr_wid.le_table_no.setText(str(self.th_get_table_no.output))

    def change_quantity(self):
        try:
            val = int(self.curr_wid.le_table_no.text().strip())
            if 0 < val < 100:
                self.MW.mess('Quantity Changed')
            else:
                raise ValueError
        except ValueError:
            self.MW.mess('Invalid Quantity')
            self.curr_wid.le_table_no.setText(str(self.th_get_table_no.output))

    def change_table_no_func(self):
        self.MW.mess('Changing...')
        self.curr_wid.bt_change.setEnabled(False)
        self.th_change_table_no.set_arg(int(self.curr_wid.le_table_no.text().strip()))
        self.th_change_table_no.start()

    def finish_change_table_no_func(self):
        self.MW.mess('Changed')
        self.get_table_no_func()
