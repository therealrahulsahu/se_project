class RunMain:
    def __init__(self, curr_wid, MW):
        self.curr_wid = curr_wid
        self.MW = MW

        from backend.threads import ThreadConnection
        self.th_connection = ThreadConnection(self)
        self.curr_wid.bt_connect.clicked.connect(self.connection_func)
        self.th_connection.signal.connect(self.finish_connection_func)
        self.connection_func()

    def connection_func(self):
        self.MW.mess('Connecting..')
        from .connection_details import mongodb_link
        self.th_connection.set_arg(mongodb_link)
        self.curr_wid.bt_connect.setEnabled(False)
        self.th_connection.start()

    def finish_connection_func(self):
        self.MW.mess('Connected')
        self.MW.select_func()
