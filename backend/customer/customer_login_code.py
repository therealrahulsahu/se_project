class RunMainLogin:
    def __init__(self, curr_wid, MW):
        self.curr_wid = curr_wid
        self.MW = MW

        self.MW.mess('Enter Customer Details ')

        self.curr_wid.bt_back.clicked.connect(self.to_back)

        from backend.customer.threads.login_code import ThreadCreateCustomer
        self.th_create_customer = ThreadCreateCustomer(self)

        self.curr_wid.bt_get_started.clicked.connect(self.to_submit)
        self.th_create_customer.signal.connect(self.to_submit_finish)

    def to_submit(self):
        self.MW.mess('Creating Customer...')

        in_name = self.curr_wid.le_name.text().strip()
        in_table_no = self.curr_wid.le_tableno.text().strip()
        in_phone = self.curr_wid.le_phone.text().strip()
        in_mail = self.curr_wid.le_mail.text().strip()

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

            self.th_create_customer.set_arg([in_name, in_table_no, in_phone, in_mail])

            from backend.dialogs import DialogConfirmation
            message_box = DialogConfirmation(dialog_script)
            message_box.resize(500, 200)
            if message_box.exec_() == DialogConfirmation.Yes:
                self.curr_wid.bt_get_started.setEnabled(False)
                self.curr_wid.bt_back.setEnabled(False)
                self.th_create_customer.start()
            else:
                self.MW.mess('Cancelled')

        except (InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError) as ob:
            self.MW.mess(str(ob))

    def to_submit_finish(self):
        self.MW.customer_func()

    def to_back(self):
        self.MW.mess('!!! Select User !!!')
        self.MW.select_func()
