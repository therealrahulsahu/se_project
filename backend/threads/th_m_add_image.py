from PyQt5.QtCore import QThread, pyqtSignal


class ThreadAddImage(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    signal_message = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        from pymongo.errors import AutoReconnect
        try:
            index = self.parent_class.curr_wid.cb_rm_food.currentIndex()
            self.food_id = self.parent_class.th_get_food_list.output_list[index]

            myc = self.parent_class.MW.DB.food
            ret_tuple = myc.find_one({'_id': self.food_id}, {'food_image': 1})
            try:
                image = ret_tuple['food_image']
                if not bool(image):
                    raise KeyError

                self.signal_message.emit(True)
            except KeyError:
                self.signal.emit(True)  # Now Proceed For upload

        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get.setEnabled(True)
