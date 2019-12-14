class RunMainStatus:
    def __init__(self, curr_wid, MW):
        self.customer_id = MW.logged_user
        self.myc_o = MW.DB.orders
        self.myc_f = MW.DB.food
        self.curr_wid = curr_wid
        self.MW = MW

        from backend.customer.threads.status import ThreadOnStatusRemoveFood, ThreadRefreshCustomerStatus
        self.th_remove = ThreadOnStatusRemoveFood(self)
        self.th_refresh = ThreadRefreshCustomerStatus(self)

        self.new_list = []

        self.curr_wid.bt_refresh_status.clicked.connect(self.refresh_func)
        self.th_refresh.signal.connect(self.finish_refresh_func)
        self.th_remove.signal.connect(self.refresh_func)
        # refresh_func()

    def refresh_func(self):
        self.new_list.clear()
        self.curr_wid.bt_refresh_status.setEnabled(False)
        self.th_refresh.start()
        self.MW.mess('Refreshing...')

    def finish_refresh_func(self):
        from backend import CommonFunctions
        CommonFunctions().clear_layout(self.curr_wid.scroll_status)

        from backend.customer.layouts import StatusMenuWidget
        if self.new_list:
            for x in self.new_list:
                self.curr_wid.scroll_status.addLayout(StatusMenuWidget(x[0], x[1], x[2], x[3], x[4], self))
            self.MW.mess('Refreshed')
        else:
            self.MW.mess('No Orders Found')
