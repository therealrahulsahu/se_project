def run_main(curr_wid, MW):
    def connection_func():
        MW.mess('Connecting..')
        from backend.customer.connection_details import mongodb_link
        th_connection.set_arg(mongodb_link)
        curr_wid.bt_connect.setEnabled(False)
        th_connection.start()

    def finish_connection_func():
        MW.mess('Connected')
        MW.select_func()

    class Variables:
        def __init__(self):
            pass

    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.threads import ThreadConnection
    th_connection = ThreadConnection(var)
    curr_wid.bt_connect.clicked.connect(connection_func)
    th_connection.signal.connect(finish_connection_func)
    connection_func()
