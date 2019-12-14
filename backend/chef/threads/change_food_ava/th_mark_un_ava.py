from PyQt5.QtCore import QThread, pyqtSignal


class ThreadMarkUnAva(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        index = self.parent_class.curr_wid.cb_food_list.currentIndex()
        to_update_id = self.parent_class.th_get_food_list.output[index]['_id']
        from pymongo.errors import AutoReconnect
        try:
            myc = self.parent_class.MW.DB.food
            ret_id = myc.update_one({'_id': to_update_id}, {'$set': {'available': False}})
            self.parent_class.MW.mess('Marked')
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get_food.setEnabled(True)
