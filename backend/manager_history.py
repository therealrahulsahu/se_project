def run_main_history(curr_wid, MW):
    # TODO: Complete history widget
    from PyQt5.QtCore import QThread, pyqtSignal
    from datetime import datetime
    curr_wid.time_start.setDateTime(datetime.now())
    curr_wid.time_end.setDateTime(datetime.now())

    class ThreadGetOrders(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.output = []

        def run(self):
            self.output.clear()
            # Sat Jan 1 00:00:00 2000
            t_start = datetime.strptime(curr_wid.time_start.dateTime().toString(), '%a %b %d %X %Y')
            t_end = datetime.strptime(curr_wid.time_end.dateTime().toString(), '%a %b %d %X %Y')
            from pymongo.errors import AutoReconnect
            from errors import InvalidTimeEntryError
            myc_o = MW.DB.orders
            try:
                if t_end < t_start:
                    raise InvalidTimeEntryError
                data_fetched = myc_o.find({'$and': [{'in_time': {'$gt': t_start}}, {'in_time': {'$lt': t_end}}]},
                                          {'_id': 1, 'in_time': 1, 'name': 1, 'order_no': 1})
                for x in data_fetched:
                    self.output.append([x['_id'], x['name'], x['order_no'], x['in_time']])
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            except InvalidTimeEntryError as ob:
                MW.mess(str(ob))
            finally:
                curr_wid.bt_get_orders.setEnabled(True)

    th_get_orders = ThreadGetOrders()

    def get_orders_func():
        MW.mess('Fetching Orders...')
        curr_wid.bt_get_orders.setEnabled(False)
        th_get_orders.run()

    def finish_get_orders_func():
        MW.mess('Orders Fetched')
        for x in th_get_orders.output:
            print(x)
            # todo complete fetching and showing

    curr_wid.bt_get_orders.clicked.connect(get_orders_func)
    th_get_orders.signal.connect(finish_get_orders_func)
