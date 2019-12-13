from PyQt5.QtCore import QThread, pyqtSignal


class ThreadGetFoodList(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output = []
        self.parent_class = parent_class

    def run(self):
        in_name = '(?i)' + self.parent_class.curr_wid.le_food_name.text().strip()
        from errors import FoodNotFoundError
        from pymongo.errors import AutoReconnect
        try:
            myc = self.parent_class.MW.DB.food
            data_list = list(
                myc.find({'name': {'$regex': in_name}}, {'_id': 1, 'name': 1, 'available': 1}).limit(10))
            if data_list:
                self.output = data_list
                self.signal.emit(True)
            else:
                raise FoodNotFoundError
        except FoodNotFoundError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get_food.setEnabled(True)
