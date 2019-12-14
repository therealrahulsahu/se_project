from PyQt5.QtCore import QThread, pyqtSignal


class ThreadTakeOrder(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def set_arg(self, customer_id, food_id, btn):
        self.customer_id = customer_id
        self.food_id = food_id
        self.btn = btn

    def run(self):
        from errors import RefreshError
        from pymongo.errors import AutoReconnect
        try:
            customer_tuple = self.parent_class.myc_o.find_one({'_id': self.customer_id},
                                            {'foods': 1, 'status_not_taken': 1, 'status_preparing': 1})
            index = customer_tuple['foods'].index(self.food_id)
            if customer_tuple['status_not_taken'][index]:
                quantity = customer_tuple['status_not_taken'][index]
                customer_tuple['status_not_taken'][index] = 0
                customer_tuple['status_preparing'][index] += quantity
                ret_id = self.parent_class.myc_o.update_one({'_id': self.customer_id}, {'$set': customer_tuple})
                self.parent_class.MW.mess('Preparing Started')
                self.signal.emit(True)
            else:
                raise RefreshError

        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        except RefreshError as ob:
            self.parent_class.MW.mess(str(ob))
            self.signal.emit(True)
        finally:
            self.btn.setEnabled(True)
