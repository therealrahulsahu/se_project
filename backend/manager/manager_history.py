def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass
    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from datetime import datetime
    curr_wid.time_start.setDateTime(datetime.now())
    curr_wid.time_end.setDateTime(datetime.now())

    from backend.manager.threads.history import ThreadGetOrdersHistory, ThreadBillHistoryFetch
    from backend.dialogs import BillDialog
    var.di_bill = BillDialog(var)

    var.th_bill_fetch = ThreadBillHistoryFetch(var)
    var.th_get_orders = ThreadGetOrdersHistory(var)

    def get_orders_func():
        MW.mess('Fetching Orders...')
        from backend import CommonFunctions
        CommonFunctions().clear_layout(curr_wid.scroll_history)
        curr_wid.bt_get_orders.setEnabled(False)
        curr_wid.bt_t_sale.setEnabled(False)
        var.th_get_orders.calling_func = 0
        var.th_get_orders.run()

    def finish_get_orders_func():
        MW.mess('Orders Fetched')
        from backend.manager.layouts import OrdersHistoryWidget
        for x in var.th_get_orders.output:
            curr_wid.scroll_history.addLayout(OrdersHistoryWidget(*x, var))

    def get_total_sale_func():
        curr_wid.bt_t_sale.setEnabled(False)
        curr_wid.bt_get_orders.setEnabled(False)
        from backend import CommonFunctions
        CommonFunctions().clear_layout(curr_wid.scroll_history)
        MW.mess('Fetching...')
        var.th_get_orders.calling_func = 1
        var.th_get_orders.run()

    def finish_get_total_sale_func():
        MW.mess('Fetched')
        from backend import CommonFunctions
        var.di_bill.set_n_run(CommonFunctions().convert_to_total_sale(var.th_get_orders.output))

    curr_wid.bt_get_orders.clicked.connect(get_orders_func)
    var.th_get_orders.signal_get_orders.connect(finish_get_orders_func)

    curr_wid.bt_t_sale.clicked.connect(get_total_sale_func)
    var.th_get_orders.signal_total_sale.connect(finish_get_total_sale_func)
