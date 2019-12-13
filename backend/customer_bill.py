class RunMainBill:
    def __init__(self, curr_wid, MW):
        self.customer_id = MW.logged_user
        self.curr_wid = curr_wid
        self.MW = MW

        from backend.threads import ThreadRefreshCustomerBill, ThreadCheckout
        self.th_refresh_bill = ThreadRefreshCustomerBill(self)
        self.th_checkout = ThreadCheckout(self)

        self.curr_wid.bt_refresh_bill.clicked.connect(self.refresh_bill_func)
        self.th_refresh_bill.signal.connect(self.finish_refresh_bill_func)

        # refresh_bill_func()

        self.curr_wid.bt_checkout.clicked.connect(self.checkout_func)
        self.th_checkout.signal.connect(self.finish_checkout)

    def refresh_bill_func(self):
        self.curr_wid.bt_refresh_bill.setEnabled(False)
        self.curr_wid.tb_bill.setText('')
        self.MW.mess('Refreshing...')
        self.th_refresh_bill.start()

    def finish_refresh_bill_func(self):
        from backend import CommonFunctions
        self.curr_wid.tb_bill.setText(
            CommonFunctions().convert_to_bill(self.th_refresh_bill.bill_doc, self.th_refresh_bill.fetch_dict))
        self.MW.mess('Refreshed')
        self.curr_wid.bt_checkout.setEnabled(True)

    def checkout_func(self):
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Are You Sure ?')
        if message_box.exec_() == message_box.Yes:
            self.curr_wid.bt_checkout.setEnabled(False)
            self.MW.mess('Finishing...')
            self.th_checkout.start()
        else:
            self.MW.mess('Cancelled')

    def finish_checkout(self):
        self.MW.mess('Thank You {}(  Your Bill {}  )'.format(' ' * 15, self.th_checkout.total_bill))
        self.MW.select_func()
