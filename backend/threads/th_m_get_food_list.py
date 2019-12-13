from PyQt5.QtCore import QThread, pyqtSignal


class ThreadFetchFoodList(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output_list = []
        self.parent_class = parent_class

    def run(self):
        in_name = r'(?i){}'.format(self.parent_class.curr_wid.le_name_query.text().strip())
        self.output_list = []
        from errors import FoodNotFoundError
        from pymongo.errors import AutoReconnect
        try:
            myc = self.parent_class.MW.DB.food
            data_list = list(myc.find({'name': {'$regex': in_name}},
                                      {'fid': 0, 'available': 0}).limit(10))
            if data_list:
                self.parent_class.curr_wid.cb_rm_food.addItems(
                    ['{0:<20} {1:<5} {2:<5} {3:<5} {4:<5}'.format(x['name'], x['region'], x['type'],
                                                                  str(x['veg']), x['price']) for x in
                     data_list])
                self.output_list = [x['_id'] for x in data_list]
                self.signal.emit(True)
            else:
                raise FoodNotFoundError
        except FoodNotFoundError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get.setEnabled(True)
