from PyQt5.QtCore import QThread, pyqtSignal


class ThreadRemoveChefQuery(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.output_list = []
        self.parent_class = parent_class

    def run(self):
        in_name = r'(?i){}'.format(self.parent_class.curr_wid.le_rm_chef.text().strip())
        self.output_list = []
        self.output_itmes = []
        from errors import ChefNotFoundError
        from pymongo.errors import AutoReconnect
        try:
            myc = self.parent_class.MW.DB.chef
            data_list = list(myc.find({'name': {'$regex': in_name}},
                                      {'password': 0, 'phone': 0}).limit(10))
            if data_list:
                self.output_itmes = data_list
                self.output_list = [x['_id'] for x in data_list]
                self.parent_class.MW.mess('List Fetched')
                self.signal.emit(True)
            else:
                self.parent_class.curr_wid.bt_rm_confirm.setEnabled(False)
                raise ChefNotFoundError
        except ChefNotFoundError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get_rm_chef.setEnabled(True)
