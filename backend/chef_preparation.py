class RunMainChefPreparation:
    def __init__(self, curr_wid, MW):
        self.curr_wid = curr_wid
        self.MW = MW
        self.myc_o = MW.DB.orders
        self.myc_f = MW.DB.food

        self.request_widget_list = []
        self.preparation_widget_list = []

        from backend.threads import ThreadTakeOrder, ThreadMarkPrepared, ThreadPreparationRefresh
        self.th_take_order = ThreadTakeOrder(self)
        self.th_mark_prepared = ThreadMarkPrepared(self)
        self.th_preparing_refresh = ThreadPreparationRefresh(self)

        self.curr_wid.bt_refresh.clicked.connect(self.refresh_func)
        self.th_preparing_refresh.signal.connect(self.finish_refresh_func)
        self.th_take_order.signal.connect(self.refresh_func)
        self.th_mark_prepared.signal.connect(self.refresh_func)
        self.refresh_func()

    def refresh_func(self):
        self.curr_wid.bt_refresh.setEnabled(False)
        from backend import CommonFunctions as Cf
        Cf().clear_layout(self.curr_wid.scroll_req)
        Cf().clear_layout(self.curr_wid.scroll_pre)
        self.request_widget_list.clear()
        self.preparation_widget_list.clear()
        self.MW.mess('Refreshing...')
        self.th_preparing_refresh.start()

    def finish_refresh_func(self):
        from backend.Layouts import RequestWidget, PreparationWidget
        for x in self.request_widget_list:
            self.curr_wid.scroll_req.addLayout(RequestWidget(*x, self))
        for x in self.preparation_widget_list:
            self.curr_wid.scroll_pre.addLayout(PreparationWidget(*x, self))
        self.MW.mess('Refreshed')
