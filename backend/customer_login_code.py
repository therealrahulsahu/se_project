def run_main(curr_wid, MW):
    MW.mess('Enter Customer Details ')

    def to_back():
        MW.mess('!!! Select User !!!')
        MW.select_func()

    curr_wid.bt_back.clicked.connect(to_back)

    def update_document(in_name, in_tableno, in_phone, in_mail):
        in_tableno = int(in_tableno)
        myc = MW.retaurant_database

    from PyQt5.QtCore import QThread, pyqtSignal

    class ThreadCreateCustomer(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            in_name = curr_wid.le_name.text().strip()
            in_tableno = curr_wid.le_tableno.text().strip()
            in_phone = curr_wid.le_phone.text().strip()
            in_mail = curr_wid.le_mail.text().strip()

            from .reg_ex_validation import validName, validPhone, validTable, validEmail
            from errors import InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError
            from pymongo.errors import AutoReconnect

            try:
                if not validName(in_name):
                    raise InvalidNameError
                if not validTable(in_tableno):
                    raise TableNoError
                if not validPhone(in_phone):
                    raise InvalidPhoneError
                if not validEmail(in_mail):
                    raise InvalidEmailError

                update_document(in_name, in_tableno, in_phone, in_mail)

                MW.mess('Welcome : ' + in_name)
                self.signal.emit(True)

            except (InvalidNameError, InvalidPhoneError, TableNoError, InvalidEmailError) as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('--> Network Error <--')
            finally:
                curr_wid.bt_get_started.setEnabled(True)

    t1_ob = ThreadCreateCustomer()

    def to_submit():
        MW.mess('Creating Customer...')
        curr_wid.bt_get_started.setEnabled(False)
        t1_ob.start()

    def to_submit_finish():
        MW.customer_func()

    curr_wid.bt_get_started.clicked.connect(to_submit)
    t1_ob.signal.connect(to_submit_finish)
