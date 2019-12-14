from PyQt5.QtCore import QThread, pyqtSignal


class ThreadRefreshCustomerStatus(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        from pymongo.errors import AutoReconnect
        myc = self.parent_class.MW.DB.orders
        try:
            return_query = {
                'foods': 1,
                'quantity': 1,
                'status_preparing': 1,
                'status_prepared': 1
            }
            order_set = myc.find_one({'_id': self.parent_class.customer_id}, return_query)

            order_set = list(zip(order_set['foods'], order_set['quantity'],
                                 order_set['status_preparing'], order_set['status_prepared']))

            myc = self.parent_class.MW.DB.food
            for x in order_set:
                ret_name = myc.find_one({'_id': x[0]}, {'name': 1})
                self.parent_class.new_list.append([x[0], ret_name['name'], x[1], x[2], x[3]])
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_refresh_status.setEnabled(True)
