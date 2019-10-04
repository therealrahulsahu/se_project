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

        def run(self):
            in_name = curr_wid.le_name.text().strip()
            in_table_no = curr_wid.le_tableno.text().strip()
            in_phone = curr_wid.le_phone.text().strip()
            in_mail = curr_wid.le_mail.text().strip()

            from .reg_ex_validation import validName, validPhone, validTable, validEmail
            from errors import InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError,\
                TableAlreadyOccupiedError, OrderNotCreatedSuccessfullyError, CustomerAlreadyInError
            from pymongo.errors import AutoReconnect

            try:
                if not validName(in_name):
                    raise InvalidNameError
                if not validTable(in_table_no):
                    raise TableNoError
                if not validPhone(in_phone):
                    raise InvalidPhoneError
                if not validEmail(in_mail):
                    raise InvalidEmailError

                from .customer_login_func_s import update_document
                update_document(in_name, in_table_no, in_phone, in_mail, MW)    # Entering data into database

                MW.mess('Welcome : ' + in_name)
                self.signal.emit(True)

            except (InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError,
                    TableAlreadyOccupiedError, OrderNotCreatedSuccessfullyError, CustomerAlreadyInError) as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('--> Network Error <--')
            finally:
                curr_wid.bt_get_started.setEnabled(True)
                curr_wid.bt_back.setEnabled(True)

    t1_ob = ThreadCreateCustomer()

    def to_submit():
        MW.mess('Creating Customer...')
        curr_wid.bt_get_started.setEnabled(False)
        curr_wid.bt_back.setEnabled(False)
        t1_ob.start()

    def to_submit_finish():
        MW.customer_func()

    curr_wid.bt_get_started.clicked.connect(to_submit)
    t1_ob.signal.connect(to_submit_finish)
