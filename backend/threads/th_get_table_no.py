from PyQt5.QtCore import QThread, pyqtSignal


class ThreadGetTableNo(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output = 0
        self.parent_class = parent_class

    def run(self):
        from pymongo.errors import AutoReconnect
        try:
            rev_data = self.parent_class.MW.DB.counter.find_one({'type': 'tables'})
            self.output = rev_data['num']
            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->>Network Error<<--')
        finally:
            self.parent_class.curr_wid.bt_change.setEnabled(True)
