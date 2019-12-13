class RunMainHistory:
    def __init__(self, curr_wid, MW):
        self.curr_wid = curr_wid
        self.MW = MW

        from datetime import datetime
        self.curr_wid.time_start.setDateTime(datetime.now())
        self.curr_wid.time_end.setDateTime(datetime.now())

        from backend.threads import ThreadBillHistoryFetch, ThreadGetOrdersHistory
        from backend.dialogs import BillDialog
        self.di_bill = BillDialog(self)
        self.th_bill_fetch = ThreadBillHistoryFetch(self)
        self.th_get_orders = ThreadGetOrdersHistory(self)

        self.curr_wid.bt_get_orders.clicked.connect(self.get_orders_func)
        self.th_get_orders.signal_get_orders.connect(self.finish_get_orders_func)

        self.curr_wid.bt_t_sale.clicked.connect(self.get_total_sale_func)
        self.th_get_orders.signal_total_sale.connect(self.finish_get_total_sale_func)

    def get_orders_func(self):
        self.MW.mess('Fetching Orders...')
        from backend import CommonFunctions
        CommonFunctions().clear_layout(self.curr_wid.scroll_history)
        self.curr_wid.bt_get_orders.setEnabled(False)
        self.curr_wid.bt_t_sale.setEnabled(False)
        self.th_get_orders.calling_func = 0
        self.th_get_orders.run()

    def finish_get_orders_func(self):
        self.MW.mess('Orders Fetched')
        from backend.Layouts import OrdersHistoryWidget
        for x in self.th_get_orders.output:
            self.curr_wid.scroll_history.addLayout(OrdersHistoryWidget(*x, self))

    def get_total_sale_func(self):
        self.curr_wid.bt_t_sale.setEnabled(False)
        self.curr_wid.bt_get_orders.setEnabled(False)
        from backend import CommonFunctions
        CommonFunctions().clear_layout(self.curr_wid.scroll_history)
        self.MW.mess('Fetching...')
        self.th_get_orders.calling_func = 1
        self.th_get_orders.run()

    def finish_get_total_sale_func(self):
        self.MW.mess('Fetched')
        from backend import CommonFunctions
        self.di_bill.set_n_run(CommonFunctions().convert_to_total_sale(self.th_get_orders.output))
