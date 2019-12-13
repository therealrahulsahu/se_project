from PyQt5.QtCore import QThread, pyqtSignal


class ThreadAddChef(QThread):
    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def set_arg(self, data):
        self.data = data

    def run(self):

        from errors import ChefAlreadyExistsError
        from pymongo.errors import AutoReconnect
        try:
            self.search_for_chef(self.data[2])
            self.add_chef_in_database(*self.data)
            self.parent_class.MW.mess(self.data[2] + ' Added')

        except ChefAlreadyExistsError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_add_chef.setEnabled(True)

    def search_for_chef(self, in_userid):
        from errors import ChefAlreadyExistsError
        myc = self.parent_class.MW.DB.chef
        data = myc.find_one({'userid': in_userid}, {'_id': 1})
        if bool(data):
            raise ChefAlreadyExistsError

    def add_chef_in_database(self, in_name, in_phone, in_userid, in_password):
        myc = self.parent_class.MW.DB.chef
        data = {
            'name': in_name,
            'userid': in_userid,
            'phone': in_phone,
            'password': in_password
        }
        ret_id = myc.insert_one(data)
