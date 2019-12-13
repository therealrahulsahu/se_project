class RunMainManageChef:
    def __init__(self, curr_wid, MW):

        self.curr_wid = curr_wid
        self.MW = MW

        self.curr_wid.bt_rm_confirm.setEnabled(False)

        from backend.threads import ThreadQueryChef, ThreadRemoveChefQuery, ThreadAddChef, ThreadRemoveChef
        self.th_query_chef = ThreadQueryChef(self)
        self.th_add_chef = ThreadAddChef(self)
        self.th_remove_chef_query = ThreadRemoveChefQuery(self)
        self.th_remove_chef = ThreadRemoveChef(self)

        self.curr_wid.bt_query_get_chef.clicked.connect(self.query_chef_func)
        self.curr_wid.bt_add_chef.clicked.connect(self.add_chef_func)
        self.curr_wid.bt_get_rm_chef.clicked.connect(self.remove_chef_query)
        self.curr_wid.bt_rm_confirm.clicked.connect(self.remove_chef_func)

        self.th_query_chef.signal.connect(self.finish_query_chef_func)
        self.th_remove_chef_query.signal.connect(self.finish_remove_chef_query)

    def list_to_string(self, data):
        css = '<style>td, th {padding: 12px;text-align: left;}</style>'
        string = '<html>{}<table><tr><th>Name</th><th>User Id</th><th>Phone</th></tr>'.format(css)
        for x in data:
            string += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(x['name'], x['userid'], x['phone'])
        string += '</table></html>'
        return string

    def query_chef_func(self):
        self.MW.mess('Fetching...')
        self.curr_wid.bt_query_get_chef.setEnabled(False)
        self.th_query_chef.start()

    def finish_query_chef_func(self):
        self.MW.mess('Data Fetched')
        data_string = self.list_to_string(self.th_query_chef.output)
        self.curr_wid.tb_chef_list.setText(data_string)

    def add_chef_func(self):
        self.MW.mess('Adding...')

        in_name = self.curr_wid.le_name.text().strip()
        in_phone = self.curr_wid.le_phone.text().strip()
        in_userid = self.curr_wid.le_userid.text().strip()
        in_password = self.curr_wid.le_password.text().strip()
        in_re_password = self.curr_wid.le_re_password.text().strip()
        from errors import InvalidNameError, InvalidPhoneError, InvalidUserIdError, \
            InvalidPasswordError, PasswordNotMatchError
        from backend import RegExValidation
        re_val = RegExValidation()
        try:
            if not re_val.validName(in_name):
                raise InvalidNameError
            if not re_val.validPhone(in_phone):
                raise InvalidPhoneError
            if not re_val.validUserId(in_userid):
                raise InvalidUserIdError
            if not re_val.validPassword(in_password):
                raise InvalidPasswordError
            if in_password != in_re_password:
                raise PasswordNotMatchError

            message_script = ('{:<10}{:<20}\n' * 4).format('Name : ', in_name,
                                                           'Phone : ', in_phone,
                                                           'User Id : ', in_userid,
                                                           'Password : ', in_password)
            from backend.dialogs import DialogConfirmation
            message_box = DialogConfirmation(message_script)
            if message_box.exec_() == message_box.Yes:
                self.th_add_chef.set_arg([in_name, in_phone, in_userid, in_password])
                self.curr_wid.bt_add_chef.setEnabled(False)
                self.th_add_chef.start()
            else:
                self.MW.mess('Cancelled')
        except (InvalidNameError, InvalidPhoneError, InvalidUserIdError,
                InvalidPasswordError, PasswordNotMatchError) as ob:
            self.MW.mess(str(ob))

    def remove_chef_query(self):
        self.MW.mess('Fetching...')
        self.curr_wid.cb_rm_chef.clear()
        self.curr_wid.bt_get_rm_chef.setEnabled(False)
        self.th_remove_chef_query.start()

    def remove_chef_func(self):
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want to Remove ?')
        if message_box.exec_() == message_box.Yes:
            self.curr_wid.bt_get_rm_chef.setEnabled(False)
            self.curr_wid.bt_rm_confirm.setEnabled(False)
            self.MW.mess('Removing...')
            self.th_remove_chef.start()
        else:
            self.MW.mess('Cancelled')

    def finish_remove_chef_query(self):
        self.curr_wid.cb_rm_chef.addItems(
            ['{0:<20} {1:<5}'.format(x['name'], x['userid']) for x in self.th_remove_chef_query.output_itmes])
        self.curr_wid.bt_rm_confirm.setEnabled(True)
