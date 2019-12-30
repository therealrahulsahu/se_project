def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass

    var = Variables()
    var.customer_id = MW.logged_user
    var.myc_o = MW.DB.orders
    var.myc_f = MW.DB.food
    var.curr_wid = curr_wid
    var.MW = MW
    var.new_list = []

    from backend.customer.threads.status import ThreadOnStatusRemoveFood, ThreadRefreshCustomerStatus
    var.th_remove = ThreadOnStatusRemoveFood(var)
    var.th_refresh = ThreadRefreshCustomerStatus(var)

    def refresh_func():
        var.new_list.clear()
        curr_wid.bt_refresh_status.setEnabled(False)
        var.th_refresh.start()
        MW.mess('Refreshing...')

    def finish_refresh_func():
        from backend import CommonFunctions
        CommonFunctions().clear_layout(curr_wid.scroll_status)

        from backend.customer.layouts import StatusMenuWidget
        if var.new_list:
            for x in var.new_list:
                curr_wid.scroll_status.addLayout(StatusMenuWidget(x[0], x[1], x[2], x[3], x[4], var))
            MW.mess('Refreshed')
        else:
            MW.mess('No Orders Found')

    curr_wid.bt_refresh_status.clicked.connect(refresh_func)
    var.th_refresh.signal.connect(finish_refresh_func)
    var.th_remove.signal.connect(refresh_func)
    # refresh_func()
