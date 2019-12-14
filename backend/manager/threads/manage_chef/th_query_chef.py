from PyQt5.QtCore import QThread, pyqtSignal


class ThreadQueryChef(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output = []
        self.parent_class = parent_class

    def run(self):
        in_query = '(?i)' + self.parent_class.curr_wid.le_query_chef.text().strip()
        myc = self.parent_class.MW.DB.chef
        from errors import ChefNotFoundError
        from pymongo.errors import AutoReconnect
        try:
            data_list = list(myc.find({'name': {'$regex': in_query}}, {'name': 1, 'userid': 1, 'phone': 1}))
            if data_list:
                self.output = data_list
                self.signal.emit(True)
            else:
                raise ChefNotFoundError
        except ChefNotFoundError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_query_get_chef.setEnabled(True)
