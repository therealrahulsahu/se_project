def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass

    var = Variables()
    var.customer_id = MW.logged_user
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.customer.threads.bill import ThreadRefreshCustomerBill, ThreadCheckout
    var.th_refresh_bill = ThreadRefreshCustomerBill(var)
    var.th_checkout = ThreadCheckout(var)

    def refresh_bill_func():
        curr_wid.bt_refresh_bill.setEnabled(False)
        curr_wid.tb_bill.setText('')
        MW.mess('Refreshing...')
        var.th_refresh_bill.start()

    def finish_refresh_bill_func():
        from backend import CommonFunctions
        curr_wid.tb_bill.setText(
            CommonFunctions().convert_to_bill(var.th_refresh_bill.bill_doc, var.th_refresh_bill.fetch_dict))
        MW.mess('Refreshed')
        curr_wid.bt_checkout.setEnabled(True)

    def checkout_func():
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Are You Sure ?')
        if message_box.exec_() == message_box.Yes:
            curr_wid.bt_checkout.setEnabled(False)
            MW.mess('Finishing...')
            var.th_checkout.start()
        else:
            MW.mess('Cancelled')

    def finish_checkout():
        MW.mess('Thank You {}(  Your Bill {}  )'.format(' ' * 15, var.th_checkout.total_bill))
        MW.select_func()

    curr_wid.bt_refresh_bill.clicked.connect(refresh_bill_func)
    var.th_refresh_bill.signal.connect(finish_refresh_bill_func)

    # refresh_bill_func()

    curr_wid.bt_checkout.clicked.connect(checkout_func)
    var.th_checkout.signal.connect(finish_checkout)