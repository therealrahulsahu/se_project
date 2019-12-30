def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass

    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.manager.threads.on_order import ThreadPaymentDone, \
        ThreadFetchBill, ThreadRefreshOnOrderStatus
    var.th_payment_done = ThreadPaymentDone(var)
    var.th_fetch_bill = ThreadFetchBill(var)
    var.th_refresh_status = ThreadRefreshOnOrderStatus(var)

    def refresh_status_func():
        curr_wid.bt_refresh_on_order.setEnabled(False)
        from backend import CommonFunctions
        CommonFunctions().clear_layout(curr_wid.scroll_on_order)
        MW.mess('Refreshing...')
        var.th_refresh_status.start()

    def finish_refresh_status_func():
        from backend.manager.layouts import OnOrderStatusWidget
        for x in var.th_refresh_status.output_list:
            curr_wid.scroll_on_order.addLayout(OnOrderStatusWidget(*x, var))
        MW.mess('Refreshed')

    def printing_bill():
        from backend import CommonFunctions
        data_to_print = CommonFunctions().convert_to_bill(var.th_fetch_bill.bill_doc, var.th_fetch_bill.fetch_dict)

        from PyQt5.QtPrintSupport import QPrintDialog
        dialog = QPrintDialog()

        from PyQt5.QtGui import QTextDocument

        doc = QTextDocument()
        doc.setHtml(data_to_print)

        if dialog.exec_() == QPrintDialog.Accepted:
            doc.print_(dialog.printer())
            MW.mess('Printing Done')
        else:
            MW.mess('Printing Rejected')

    curr_wid.bt_refresh_on_order.clicked.connect(refresh_status_func)
    var.th_refresh_status.signal.connect(finish_refresh_status_func)
    refresh_status_func()
    var.th_payment_done.signal.connect(refresh_status_func)
    var.th_fetch_bill.signal.connect(printing_bill)
