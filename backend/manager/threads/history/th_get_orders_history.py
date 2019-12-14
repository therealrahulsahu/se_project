from PyQt5.QtCore import QThread, pyqtSignal


class ThreadGetOrdersHistory(QThread):
    signal_get_orders = pyqtSignal('PyQt_PyObject')
    signal_total_sale = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output = []
        self.calling_func = 0
        self.parent_class = parent_class

    def run(self):
        self.output.clear()
        # Sat Jan 1 00:00:00 2000
        from datetime import datetime
        t_start = datetime.strptime(self.parent_class.curr_wid.time_start.dateTime().toString(), '%a %b %d %X %Y')
        t_end = datetime.strptime(self.parent_class.curr_wid.time_end.dateTime().toString(), '%a %b %d %X %Y')
        from pymongo.errors import AutoReconnect
        from errors import InvalidTimeEntryError, NoOrdersFoundError
        myc_o = self.parent_class.MW.DB.orders
        try:
            if t_end < t_start:
                raise InvalidTimeEntryError
            in_time_query = {'$and': [{'in_time': {'$gt': t_start}}, {'in_time': {'$lt': t_end}}],
                             'pay_done': True}
            if self.calling_func == 0:
                data_fetched = myc_o.find(in_time_query,
                                          {'_id': 1, 'in_time': 1, 'name': 1, 'order_no': 1})
                for x in data_fetched:
                    self.output.append([x['_id'], x['name'], x['order_no'], x['in_time'], True])
                if not self.output:
                    raise NoOrdersFoundError
                self.signal_get_orders.emit(True)
            else:
                data_fetched = myc_o.find(in_time_query,
                                          {'in_time': 1, 'name': 1, 'order_no': 1, 'total': 1})
                count = 1
                for x in data_fetched:
                    self.output.append([count, x['name'], x['order_no'],
                                        x['in_time'].strftime('%c'), x['total']])
                    count += 1
                if not self.output:
                    raise NoOrdersFoundError
                self.signal_total_sale.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        except (InvalidTimeEntryError, NoOrdersFoundError) as ob:
            self.parent_class.MW.mess(str(ob))
        finally:
            self.parent_class.curr_wid.bt_get_orders.setEnabled(True)
            self.parent_class.curr_wid.bt_t_sale.setEnabled(True)
