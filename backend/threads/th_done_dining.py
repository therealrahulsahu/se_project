from PyQt5.QtCore import QThread, pyqtSignal


class ThreadDoneDining(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    fail_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        from pymongo.errors import AutoReconnect
        try:
            self.data_entry(self.parent_class.selected_food_list)

            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.fail_signal.emit(True)

    def data_entry(self, data_list):

        def data_convert(data):
            new_data = [{
                'foods': x.DB_id,
                'quantity': int(x.quantity),
                'price': int(x.food_price)
            } for x in data]
            return new_data

        data_list = data_convert(data_list)

        myc = self.parent_class.MW.DB.orders
        customer_id = self.parent_class.MW.logged_user
        query_return = {'foods': 1,
                        'quantity': 1,
                        'status_not_taken': 1,
                        'status_preparing': 1,
                        'status_prepared': 1,
                        'total': 1
                        }
        fetched_data = myc.find_one({'_id': customer_id}, query_return)

        def update_data(data):
            for x in data:
                if x['foods'] in fetched_data['foods']:
                    ind = fetched_data['foods'].index(x['foods'])
                    fetched_data['quantity'][ind] += x['quantity']
                    fetched_data['status_not_taken'][ind] += x['quantity']
                    fetched_data['total'] += x['price'] * x['quantity']
                else:
                    fetched_data['foods'].append(x['foods'])
                    fetched_data['quantity'].append(x['quantity'])
                    fetched_data['status_not_taken'].append(x['quantity'])
                    fetched_data['status_preparing'].append(0)
                    fetched_data['status_prepared'].append(0)
                    fetched_data['total'] += x['price'] * x['quantity']

        update_data(data_list)
        return_id = myc.update_one({'_id': customer_id}, {'$set': fetched_data})
