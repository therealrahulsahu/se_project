def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass
    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.manager.threads.restau import ThreadGetTableNo, ThreadChangeTableNo
    var.th_get_table_no = ThreadGetTableNo(var)
    var.th_change_table_no = ThreadChangeTableNo(var)

    def get_table_no_func():
        MW.mess('Fetching...')
        curr_wid.bt_change.setEnabled(False)
        var.th_get_table_no.start()

    def finish_get_table_no_func():
        MW.mess('Fetched')
        curr_wid.lb_table_no_2.setText(str(var.th_get_table_no.output))
        curr_wid.le_table_no.setText(str(var.th_get_table_no.output))

    def change_quantity():
        try:
            val = int(curr_wid.le_table_no.text().strip())
            if 0 < val < 100:
                MW.mess('Quantity Changed')
            else:
                raise ValueError
        except ValueError:
            MW.mess('Invalid Quantity')
            curr_wid.le_table_no.setText(str(var.th_get_table_no.output))

    def change_table_no_func():
        MW.mess('Changing...')
        curr_wid.bt_change.setEnabled(False)
        var.th_change_table_no.set_arg(int(curr_wid.le_table_no.text().strip()))
        var.th_change_table_no.start()

    def finish_change_table_no_func():
        MW.mess('Changed')
        get_table_no_func()

    var.th_get_table_no.signal.connect(finish_get_table_no_func)
    get_table_no_func()
    curr_wid.le_table_no.editingFinished.connect(change_quantity)
    curr_wid.bt_change.clicked.connect(change_table_no_func)
    var.th_change_table_no.signal.connect(finish_change_table_no_func)
