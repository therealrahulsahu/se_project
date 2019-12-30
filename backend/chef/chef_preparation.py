def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass
    var = Variables()

    var.curr_wid = curr_wid
    var.MW = MW
    var.myc_o = MW.DB.orders
    var.myc_f = MW.DB.food

    var.request_widget_list = []
    var.preparation_widget_list = []

    from backend.chef.threads.preparation import ThreadTakeOrder, \
        ThreadMarkPrepared, ThreadPreparationRefresh
    var.th_take_order = ThreadTakeOrder(var)
    var.th_mark_prepared = ThreadMarkPrepared(var)
    var.th_preparing_refresh = ThreadPreparationRefresh(var)

    def refresh_func():
        curr_wid.bt_refresh.setEnabled(False)
        from backend import CommonFunctions as Cf
        Cf().clear_layout(curr_wid.scroll_req)
        Cf().clear_layout(curr_wid.scroll_pre)
        var.request_widget_list.clear()
        var.preparation_widget_list.clear()
        MW.mess('Refreshing...')
        var.th_preparing_refresh.start()

    def finish_refresh_func():
        from backend.chef.layouts import RequestWidget, PreparationWidget
        for x in var.request_widget_list:
            curr_wid.scroll_req.addLayout(RequestWidget(*x, var))
        for x in var.preparation_widget_list:
            curr_wid.scroll_pre.addLayout(PreparationWidget(*x, var))
        MW.mess('Refreshed')

    curr_wid.bt_refresh.clicked.connect(refresh_func)
    var.th_preparing_refresh.signal.connect(finish_refresh_func)
    var.th_take_order.signal.connect(refresh_func)
    var.th_mark_prepared.signal.connect(refresh_func)
    refresh_func()
