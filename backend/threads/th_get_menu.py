from PyQt5.QtCore import QThread, pyqtSignal


class ThreadGetMenu(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        if self.check_for_veg():
            food_query = {
                'veg': True,
                'region': self.check_for_region(),
                'type': self.check_for_type(),
                'available': True
            }
        else:
            food_query = {
                'region': self.check_for_region(),
                'type': self.check_for_type(),
                'available': True
            }

        myc = self.parent_class.MW.DB.food
        from pymongo.errors import AutoReconnect
        from errors import FoodNotFoundError
        try:
            data_list = list(myc.find(food_query, {'_id': 1, 'name': 1, 'price': 1}))
            if data_list:
                self.parent_class.searched_food_list = data_list
                self.signal.emit(True)
            else:
                raise FoodNotFoundError
        except FoodNotFoundError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get.setEnabled(True)

    def check_for_veg(self):
        return self.parent_class.curr_wid.rbt_veg.isChecked()

    def check_for_region(self):
        if self.parent_class.curr_wid.rbt_north_ind.isChecked():
            return 'nid'
        elif self.parent_class.curr_wid.rbt_italian.isChecked():
            return 'ita'
        elif self.parent_class.curr_wid.rbt_south_ind.isChecked():
            return 'sid'
        elif self.parent_class.curr_wid.rbt_conti.isChecked():
            return 'conti'
        elif self.parent_class.curr_wid.rbt_thai.isChecked():
            return 'thi'
        elif self.parent_class.curr_wid.rbt_china.isChecked():
            return 'chi'
        elif self.parent_class.curr_wid.rbt_rajas.isChecked():
            return 'raj'
        elif self.parent_class.curr_wid.rbt_none.isChecked():
            return 'none'

    def check_for_type(self):
        if self.parent_class.curr_wid.rbt_starter.isChecked():
            return 'sta'
        elif self.parent_class.curr_wid.rbt_main.isChecked():
            return 'mcs'
        elif self.parent_class.curr_wid.rbt_refresh.isChecked():
            return 'ref'
        elif self.parent_class.curr_wid.rbt_dessert.isChecked():
            return 'des'
        elif self.parent_class.curr_wid.rbt_bread.isChecked():
            return 'bre'
