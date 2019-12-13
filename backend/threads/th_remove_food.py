from PyQt5.QtCore import QThread, pyqtSignal


class ThreadOnStatusRemoveFood(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def set_arg(self, rm_id, rm_quan, remove_btn):
        self.rm_id = rm_id
        self.rm_quan = rm_quan
        self.remove_btn = remove_btn

    def run(self):
        from pymongo.errors import AutoReconnect
        from errors import CantRemoveOrderPreparingError
        try:
            return_query = {
                'foods': 1,
                'quantity': 1,
                'status_not_taken': 1,
                'status_preparing': 1,
                'status_prepared': 1,
                'total': 1
            }
            fetched_order = self.parent_class.myc_o.find_one({'_id': self.parent_class.customer_id}, return_query)

            f_price = self.parent_class.myc_f.find_one({'_id': self.rm_id}, {'price': 1})
            f_price = f_price['price']

            ind = fetched_order['foods'].index(self.rm_id)
            if self.rm_quan == fetched_order['status_not_taken'][ind] and \
                    fetched_order['status_preparing'][ind] == 0 and fetched_order['status_prepared'][ind] == 0:
                fetched_order['foods'].pop(ind)
                fetched_order['quantity'].pop(ind)
                fetched_order['status_not_taken'].pop(ind)
                fetched_order['status_preparing'].pop(ind)
                fetched_order['status_prepared'].pop(ind)
                fetched_order['total'] -= self.rm_quan * f_price

                ret_id = self.parent_class.myc_o.update_one({'_id': self.parent_class.customer_id},
                                                            {'$set': fetched_order})
                self.parent_class.MW.mess('Food Removed')
                self.signal.emit(True)
            elif self.rm_quan <= fetched_order['status_not_taken'][ind]:
                fetched_order['quantity'][ind] -= self.rm_quan
                fetched_order['status_not_taken'][ind] -= self.rm_quan
                fetched_order['total'] -= self.rm_quan * f_price

                ret_id = self.parent_class.myc_o.update_one({'_id': self.parent_class.customer_id},
                                                            {'$set': fetched_order})
                self.parent_class.MW.mess('Food Removed')
                self.signal.emit(True)
            else:
                raise CantRemoveOrderPreparingError

        except CantRemoveOrderPreparingError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error<<--')
        finally:
            self.remove_btn.setEnabled(True)
