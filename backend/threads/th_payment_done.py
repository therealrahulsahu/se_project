from PyQt5.QtCore import QThread, pyqtSignal


class ThreadPaymentDone(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def set_srg(self, btn, customer_id):
        self.btn = btn
        self.customer_id = customer_id

    def run(self):
        from pymongo.errors import AutoReconnect
        from errors import RefreshError, CustomerNotDoneYetError
        myc_o = self.parent_class.MW.DB.orders
        try:
            customer_data = myc_o.find_one({'_id': self.customer_id},
                                           {'done': 1, 'pay_done': 1, 'out_time': 1})
            if not customer_data['done']:
                raise CustomerNotDoneYetError
            if customer_data['pay_done']:
                raise RefreshError
            from datetime import datetime
            customer_data['pay_done'] = True
            customer_data['out_time'] = datetime.now()
            ret_id = myc_o.update_one({'_id': self.customer_id}, {'$set': customer_data})
            self.parent_class.MW.mess('Payment Done')
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error  <<--')
        except RefreshError as ob:
            self.parent_class.MW.mess(str(ob))
            self.signal.emit(True)
        except CustomerNotDoneYetError as ob:
            self.parent_class.MW.mess(str(ob))
        finally:
            self.btn.setEnabled(True)
