def run_main(curr_wid, MW):
    MW.mess('Enter Customer Details ')

    def to_back():
        MW.mess('!!! Select User !!!')
        MW.select_func()

    curr_wid.bt_back.clicked.connect(to_back)

    from PyQt5.QtCore import QThread, pyqtSignal

    class ThreadCreateCustomer(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def set_arg(self, data):
            self.data = data

        def run(self):

            from errors import CustomerAlreadyInError, TableAlreadyOccupiedError, OrderNotCreatedSuccessfullyError
            from pymongo.errors import AutoReconnect

            try:
                from .customer_login_func_s import update_document
                update_document(*self.data, MW)    # Entering data into database

                MW.mess('Welcome : ' + self.data[0])
                self.signal.emit(True)

            except (TableAlreadyOccupiedError, OrderNotCreatedSuccessfullyError) as ob:
                MW.mess(str(ob))
            except CustomerAlreadyInError as ob:
                MW.mess(str(ob))
                MW.logged_user = ob.customer_id
                MW.mess('Welcome Back: ' + ob.name)
                self.signal.emit(True)

            except AutoReconnect:
                MW.mess('--> Network Error <--')
            finally:
                curr_wid.bt_get_started.setEnabled(True)
                curr_wid.bt_back.setEnabled(True)

    th_create_customer = ThreadCreateCustomer()

    def to_submit():
        MW.mess('Creating Customer...')

        in_name = curr_wid.le_name.text().strip()
        in_table_no = curr_wid.le_tableno.text().strip()
        in_phone = curr_wid.le_phone.text().strip()
        in_mail = curr_wid.le_mail.text().strip()

        dialog_script = ('{:<10}{:<25}\n'*4).format('Name : ', in_name,
                                                    'Table No.: ', in_table_no,
                                                    'Phone No. ', in_phone,
                                                    'Mail : ', in_mail)
        from .reg_ex_validation import validName, validPhone, validTable, validEmail
        from errors import InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError

        try:
            if not validName(in_name):
                raise InvalidNameError
            if not validTable(in_table_no):
                raise TableNoError
            if not validPhone(in_phone):
                raise InvalidPhoneError
            if not validEmail(in_mail):
                raise InvalidEmailError

            th_create_customer.set_arg([in_name, in_table_no, in_phone, in_mail])

            from .common_functions import DialogConfirmation
            message_box = DialogConfirmation(dialog_script)
            message_box.resize(500, 200)
            if message_box.exec_() == DialogConfirmation.Yes:
                curr_wid.bt_get_started.setEnabled(False)
                curr_wid.bt_back.setEnabled(False)
                th_create_customer.start()
            else:
                MW.mess('Cancelled')

        except (InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError) as ob:
            MW.mess(str(ob))

    def to_submit_finish():
        MW.customer_func()

    curr_wid.bt_get_started.clicked.connect(to_submit)
    th_create_customer.signal.connect(to_submit_finish)
