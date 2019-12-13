from PyQt5.QtCore import QThread, pyqtSignal


class ThreadRemoveChef(QThread):
    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        from pymongo.errors import AutoReconnect
        try:
            index = self.parent_class.curr_wid.cb_rm_chef.currentIndex()
            to_be_delete_id = self.parent_class.th_remove_chef_query.output_list[index]

            myc = self.parent_class.MW.DB.chef
            ret_del = myc.delete_one({'_id': to_be_delete_id})
            self.parent_class.curr_wid.cb_rm_chef.clear()
            self.parent_class.MW.mess('Removed')
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_get_rm_chef.setEnabled(True)
