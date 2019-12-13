from PyQt5.QtCore import QThread, pyqtSignal


class ThreadFetchBill(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.bill_doc = []
        self.parent_class = parent_class

    def set_arg(self, customer_id, btn):
        self.customer_id = customer_id
        self.btn = btn

    def run(self):
        self.bill_doc = []
        self.fetch_dict = dict()
        from pymongo.errors import AutoReconnect
        from errors import NoOrdersFoundError
        try:
            myc_o = self.parent_class.MW.DB.orders
            myc_f = self.parent_class.MW.DB.food
            order_data = myc_o.find_one({'_id': self.customer_id},
                                        {'name': 1, 'order_no': 1, 'phone': 1, 'mail': 1, 'table_no': 1,
                                         'foods': 1, 'quantity': 1, 'total': 1, 'in_time': 1, 'out_time': 1})
            self.fetch_dict = order_data
            order_data = list(zip(order_data['foods'], order_data['quantity']))
            for x in order_data:
                food_detail = myc_f.find_one({'_id': x[0]}, {'name': 1, 'price': 1})
                self.bill_doc.append(
                    [food_detail['name'], food_detail['price'], x[1], food_detail['price'] * x[1]])
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        except NoOrdersFoundError as ob:
            self.parent_class.MW.mess(str(ob))
        finally:
            self.btn.setEnabled(True)
