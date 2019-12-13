from PyQt5.QtCore import QThread, pyqtSignal


class ThreadFetchImage(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output = b''
        self.parent_class = parent_class

    def set_arg(self, btn, ob_id, food_name):
        self.btn = btn
        self.ob_id = ob_id
        self.food_name = food_name

    def run(self):
        self.output = b''
        from pymongo.errors import AutoReconnect
        from errors import ImageNotAvailableError
        myc_f = self.parent_class.MW.DB.food
        try:
            ret_tuple = myc_f.find_one({'_id': self.ob_id}, {'food_image': 1})
            try:
                self.output = ret_tuple['food_image']
                if not self.output:
                    raise ImageNotAvailableError
            except KeyError:
                raise ImageNotAvailableError
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        except ImageNotAvailableError as ob:
            self.parent_class.MW.mess(str(ob))
        finally:
            self.btn.setEnabled(True)
