def run_main_manage_chef(curr_wid, MW):
    from PyQt5.QtCore import QThread, pyqtSignal

    def list_to_string(data):
        css = '<style>td, th {padding: 12px;text-align: left;}</style>'
        string = '<html>{}<table><tr><th>Name</th><th>User Id</th><th>Phone</th></tr>'.format(css)
        for x in data:
            string += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(x['name'], x['userid'], x['phone'])
        string += '</table></html>'
        return string

    def search_for_chef(in_userid):
        from errors import ChefAlreadyExistsError
        myc = MW.DB.chef
        data = myc.find_one({'userid': in_userid}, {'_id': 1})
        if bool(data):
            raise ChefAlreadyExistsError

    def add_chef_in_database(in_name, in_phone, in_userid, in_password):
        myc = MW.DB.chef
        data = {
            'name': in_name,
            'userid': in_userid,
            'phone': in_phone,
            'password': in_password
        }
        ret_id = myc.insert_one(data)

    class ThreadQueryChef(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.output = []

        def run(self):
            in_query = '(?i)' + curr_wid.le_query_chef.text().strip()
            myc = MW.DB.chef
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
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_query_get_chef.setEnabled(True)

    class ThreadAddChef(QThread):
        def __init__(self):
            super().__init__()

        def run(self):
            in_name = curr_wid.le_name.text().strip()
            in_phone = curr_wid.le_phone.text().strip()
            in_userid = curr_wid.le_userid.text().strip()
            in_password = curr_wid.le_password.text().strip()
            in_re_password = curr_wid.le_re_password.text().strip()
            from pymongo.errors import AutoReconnect
            from errors import InvalidNameError, InvalidPhoneError, InvalidUserIdError, \
                InvalidPasswordError, PasswordNotMatchError, ChefAlreadyExistsError
            from .reg_ex_validation import validName, validPhone, validUserId, validPassword
            try:
                if not validName(in_name):
                    raise InvalidNameError
                if not validPhone(in_phone):
                    raise InvalidPhoneError
                if not validUserId(in_userid):
                    raise InvalidUserIdError
                if not validPassword(in_password):
                    raise InvalidPasswordError
                if in_password != in_re_password:
                    raise PasswordNotMatchError

                search_for_chef(in_userid)
                add_chef_in_database(in_name, in_phone, in_userid, in_password)
                MW.mess(in_userid + ' Added')
            except (InvalidNameError, InvalidPhoneError, InvalidUserIdError,
                    InvalidPasswordError, PasswordNotMatchError, ChefAlreadyExistsError) as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_add_chef.setEnabled(True)

    class ThreadRemoveChefQuery(QThread):

        def __init__(self):
            super().__init__()
            self.output_list = []

        def run(self):
            in_name = r'(?i){}'.format(curr_wid.le_rm_chef.text().strip())
            self.output_list = []
            from errors import ChefNotFoundError
            from pymongo.errors import AutoReconnect
            try:
                myc = MW.DB.chef
                data_list = list(myc.find({'name': {'$regex': in_name}},
                                          {'password': 0, 'phone': 0}).limit(10))
                if data_list:
                    curr_wid.cb_rm_chef.addItems(
                        ['{0:<20} {1:<5}'.format(x['name'], x['userid']) for x in data_list])
                    self.output_list = [x['_id'] for x in data_list]
                    curr_wid.bt_rm_confirm.setEnabled(True)
                    MW.mess('List Fetched')
                else:
                    curr_wid.bt_rm_confirm.setEnabled(False)
                    raise ChefNotFoundError
            except ChefNotFoundError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get_rm_chef.setEnabled(True)

    class ThreadRemoveChef(QThread):
        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            try:
                index = curr_wid.cb_rm_chef.currentIndex()
                to_be_delete_id = th_remove_chef_query.output_list[index]

                myc = MW.DB.chef
                ret_del = myc.delete_one({'_id': to_be_delete_id})
                curr_wid.cb_rm_chef.clear()
                MW.mess('Removed')
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get_rm_chef.setEnabled(True)

    curr_wid.bt_rm_confirm.setEnabled(False)

    th_query_chef = ThreadQueryChef()
    th_add_chef = ThreadAddChef()
    th_remove_chef_query = ThreadRemoveChefQuery()
    th_remove_chef = ThreadRemoveChef()

    def query_chef_func():
        MW.mess('Fetching...')
        curr_wid.bt_query_get_chef.setEnabled(False)
        th_query_chef.start()

    def finish_query_chef_func():
        MW.mess('Data Fetched')
        data_string = list_to_string(th_query_chef.output)
        curr_wid.tb_chef_list.setText(data_string)

    def add_chef_func():
        MW.mess('Adding...')
        curr_wid.bt_add_chef.setEnabled(False)
        th_add_chef.start()

    def remove_chef_query():
        MW.mess('Fetching...')
        curr_wid.cb_rm_chef.clear()
        curr_wid.bt_get_rm_chef.setEnabled(False)
        th_remove_chef_query.start()

    def remove_chef_func():
        from .common_functions import DialogConfirmation
        message_box = DialogConfirmation('Do You Want to Remove ?')
        if message_box.exec_() == message_box.Yes:
            curr_wid.bt_get_rm_chef.setEnabled(False)
            curr_wid.bt_rm_confirm.setEnabled(False)
            MW.mess('Removing...')
            th_remove_chef.start()
        else:
            MW.mess('Cancelled')

    curr_wid.bt_query_get_chef.clicked.connect(query_chef_func)
    curr_wid.bt_add_chef.clicked.connect(add_chef_func)
    curr_wid.bt_get_rm_chef.clicked.connect(remove_chef_query)
    curr_wid.bt_rm_confirm.clicked.connect(remove_chef_func)

    th_query_chef.signal.connect(finish_query_chef_func)
