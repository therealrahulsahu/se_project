from PyQt5.QtCore import QThread, pyqtSignal


class ThreadChangeTableNo(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.num = 0
        self.parent_class = parent_class

    def set_arg(self, num):
        self.num = num

    def run(self):
        from pymongo.errors import AutoReconnect
        try:
            rev_ids = self.parent_class.MW.DB.counter.update_one({'type': 'tables'}, {'$set': {'num': self.num}})
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->>Network Error<<--')
        finally:
            self.parent_class.curr_wid.bt_change.setEnabled(True)
