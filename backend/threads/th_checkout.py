from PyQt5.QtCore import QThread, pyqtSignal


class ThreadCheckout(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.total_bill = 0
        self.parent_class = parent_class

    def run(self):
        from pymongo.errors import AutoReconnect
        from errors import SomeOrdersPreparingError, NoOrdersFoundError
        myc_o = self.parent_class.MW.DB.orders
        try:
            order = myc_o.find_one({'_id': self.parent_class.customer_id}, {'quantity': 1, 'status_not_taken': 1,
                                                          'done': 1, 'total': 1})
            self.total_bill = order['total']
            if any(order['status_not_taken']):
                raise SomeOrdersPreparingError
            elif not len(order['quantity']):
                raise NoOrdersFoundError
            else:
                order['done'] = True
                ret_id = myc_o.update_one({'_id': self.parent_class.customer_id}, {'$set': order})
                self.signal.emit(True)

        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        except (SomeOrdersPreparingError, NoOrdersFoundError) as ob:
            self.parent_class.MW.mess(str(ob))
        finally:
            self.parent_class.curr_wid.bt_checkout.setEnabled(True)
