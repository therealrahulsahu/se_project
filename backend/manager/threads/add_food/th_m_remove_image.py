from PyQt5.QtCore import QThread, pyqtSignal


class ThreadRemoveImage(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        from pymongo.errors import AutoReconnect
        try:
            index = self.parent_class.curr_wid.cb_rm_food.currentIndex()
            food_id = self.parent_class.th_get_food_list.output_list[index]

            myc = self.parent_class.MW.DB.food
            ret_id = myc.update_one({'_id': food_id}, {'$set': {'food_image': b''}})
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get.setEnabled(True)
