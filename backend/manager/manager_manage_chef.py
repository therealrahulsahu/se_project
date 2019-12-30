def run_main(curr_wid, MW):

    class Variable:
        def __init__(self):
            pass

    var = Variable()
    var.curr_wid = curr_wid
    var.MW = MW

    curr_wid.bt_rm_confirm.setEnabled(False)

    from backend.manager.threads.manage_chef import ThreadQueryChef, ThreadRemoveChefQuery, \
        ThreadAddChef, ThreadRemoveChef
    var.th_query_chef = ThreadQueryChef(var)
    var.th_add_chef = ThreadAddChef(var)
    var.th_remove_chef_query = ThreadRemoveChefQuery(var)
    var.th_remove_chef = ThreadRemoveChef(var)

    def list_to_string(data):
        css = '<style>td, th {padding: 12px;text-align: left;}</style>'
        string = '<html>{}<table><tr><th>Name</th><th>User Id</th><th>Phone</th></tr>'.format(css)
        for x in data:
            string += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(x['name'], x['userid'], x['phone'])
        string += '</table></html>'
        return string

    def query_chef_func():
        MW.mess('Fetching...')
        curr_wid.bt_query_get_chef.setEnabled(False)
        var.th_query_chef.start()

    def finish_query_chef_func():
        MW.mess('Data Fetched')
        data_string = list_to_string(var.th_query_chef.output)
        curr_wid.tb_chef_list.setText(data_string)

    def add_chef_func():
        MW.mess('Adding...')

        in_name = curr_wid.le_name.text().strip()
        in_phone = curr_wid.le_phone.text().strip()
        in_userid = curr_wid.le_userid.text().strip()
        in_password = curr_wid.le_password.text().strip()
        in_re_password = curr_wid.le_re_password.text().strip()
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
                var.th_add_chef.set_arg([in_name, in_phone, in_userid, in_password])
                curr_wid.bt_add_chef.setEnabled(False)
                var.th_add_chef.start()
            else:
                MW.mess('Cancelled')
        except (InvalidNameError, InvalidPhoneError, InvalidUserIdError,
                InvalidPasswordError, PasswordNotMatchError) as ob:
            MW.mess(str(ob))

    def remove_chef_query():
        MW.mess('Fetching...')
        curr_wid.cb_rm_chef.clear()
        curr_wid.bt_get_rm_chef.setEnabled(False)
        var.th_remove_chef_query.start()

    def remove_chef_func():
        from backend.dialogs import DialogConfirmation
        message_box = DialogConfirmation('Do You Want to Remove ?')
        if message_box.exec_() == message_box.Yes:
            curr_wid.bt_get_rm_chef.setEnabled(False)
            curr_wid.bt_rm_confirm.setEnabled(False)
            MW.mess('Removing...')
            var.th_remove_chef.start()
        else:
            MW.mess('Cancelled')

    def finish_remove_chef_query():
        curr_wid.cb_rm_chef.addItems(
            ['{0:<20} {1:<5}'.format(x['name'], x['userid']) for x in var.th_remove_chef_query.output_itmes])
        curr_wid.bt_rm_confirm.setEnabled(True)

    curr_wid.bt_query_get_chef.clicked.connect(query_chef_func)
    curr_wid.bt_add_chef.clicked.connect(add_chef_func)
    curr_wid.bt_get_rm_chef.clicked.connect(remove_chef_query)
    curr_wid.bt_rm_confirm.clicked.connect(remove_chef_func)

    var.th_query_chef.signal.connect(finish_query_chef_func)
    var.th_remove_chef_query.signal.connect(finish_remove_chef_query)
