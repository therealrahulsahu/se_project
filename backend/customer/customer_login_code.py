def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass
    var = Variables()

    var.curr_wid = curr_wid
    var.MW = MW

    from backend.customer.threads.login_code import ThreadCreateCustomer
    var.th_create_customer = ThreadCreateCustomer(var)

    MW.mess('Enter Customer Details ')

    def to_submit():
        MW.mess('Creating Customer...')

        in_name = curr_wid.le_name.text().strip()
        in_table_no = curr_wid.le_tableno.text().strip()
        in_phone = curr_wid.le_phone.text().strip()
        in_mail = curr_wid.le_mail.text().strip()

        dialog_script = ('{:<10}{:<25}\n' * 4).format('Name : ', in_name,
                                                      'Table No.: ', in_table_no,
                                                      'Phone No. ', in_phone,
                                                      'Mail : ', in_mail)
        from backend import RegExValidation
        re_val = RegExValidation()
        from errors import InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError

        try:
            if not re_val.validName(in_name):
                raise InvalidNameError
            if not re_val.validTable(in_table_no):
                raise TableNoError
            if not re_val.validPhone(in_phone):
                raise InvalidPhoneError
            if not re_val.validEmail(in_mail):
                raise InvalidEmailError

            var.th_create_customer.set_arg([in_name, in_table_no, in_phone, in_mail])

            from backend.dialogs import DialogConfirmation
            message_box = DialogConfirmation(dialog_script)
            message_box.resize(500, 200)
            if message_box.exec_() == DialogConfirmation.Yes:
                curr_wid.bt_get_started.setEnabled(False)
                curr_wid.bt_back.setEnabled(False)
                var.th_create_customer.start()
            else:
                MW.mess('Cancelled')

        except (InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError) as ob:
            MW.mess(str(ob))

    def to_submit_finish():
        MW.customer_func()

    def to_back():
        MW.mess('!!! Select User !!!')
        MW.select_func()

    curr_wid.bt_back.clicked.connect(to_back)
    curr_wid.bt_get_started.clicked.connect(to_submit)
    var.th_create_customer.signal.connect(to_submit_finish)
