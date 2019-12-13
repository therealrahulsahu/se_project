from PyQt5.QtCore import QThread, pyqtSignal


class ThreadRefreshOnOrderStatus(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output_list = []
        self.parent_class = parent_class

    def run(self):
        self.output_list.clear()
        from pymongo.errors import AutoReconnect
        from errors import CustomerNotDoneYetError
        myc_o = self.parent_class.MW.DB.orders
        try:
            customers_data = myc_o.find({'pay_done': False},
                                        {'_id': 1, 'name': 1, 'table_no': 1, 'done': 1, 'total': 1})
            for x in customers_data:
                self.output_list.append([x['_id'], x['name'], x['table_no'], x['done'], x['total']])
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        except CustomerNotDoneYetError as ob:
            self.parent_class.MW.mess(str(ob))
        finally:
            self.parent_class.curr_wid.bt_refresh_on_order.setEnabled(True)
