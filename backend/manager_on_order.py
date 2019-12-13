class RunMainOnOrder:
    def __init__(self, curr_wid, MW):
        self.curr_wid = curr_wid
        self.MW = MW

        from backend.threads import ThreadPaymentDone, ThreadFetchBill, ThreadRefreshOnOrderStatus
        self.th_payment_done = ThreadPaymentDone(self)

        self.th_fetch_bill = ThreadFetchBill(self)

        self.th_refresh_status = ThreadRefreshOnOrderStatus(self)

        curr_wid.bt_refresh_on_order.clicked.connect(self.refresh_status_func)
        self.th_refresh_status.signal.connect(self.finish_refresh_status_func)
        self.refresh_status_func()
        self.th_payment_done.signal.connect(self.refresh_status_func)
        self.th_fetch_bill.signal.connect(self.printing_bill)

    def refresh_status_func(self):
        self.curr_wid.bt_refresh_on_order.setEnabled(False)
        from backend import CommonFunctions
        CommonFunctions().clear_layout(self.curr_wid.scroll_on_order)
        self.MW.mess('Refreshing...')
        self.th_refresh_status.start()

    def finish_refresh_status_func(self):
        from backend.Layouts import OnOrderStatusWidget
        for x in self.th_refresh_status.output_list:
            self.curr_wid.scroll_on_order.addLayout(OnOrderStatusWidget(*x, self))
        self.MW.mess('Refreshed')

    def printing_bill(self):
        from backend import CommonFunctions
        data_to_print = CommonFunctions().convert_to_bill(self.th_fetch_bill.bill_doc, self.th_fetch_bill.fetch_dict)

        from PyQt5.QtPrintSupport import QPrintDialog
        dialog = QPrintDialog()

        from PyQt5.QtGui import QTextDocument

        doc = QTextDocument()
        doc.setHtml(data_to_print)

        if dialog.exec_() == QPrintDialog.Accepted:
            doc.print_(dialog.printer())
            self.MW.mess('Printing Done')
        else:
            self.MW.mess('Printing Rejected')
