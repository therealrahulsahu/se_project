def run_main(curr_wid, MW):
    MW.mess('Enter Customer Details ')

    def to_back():
        MW.mess('!!! Select User !!!')
        MW.select_func()

    curr_wid.bt_back.clicked.connect(to_back)

    def check_table_counter(in_table_no):
        from errors import TableNoError
        myc = MW.myc.retaurant_database.counter
        table_count = myc.find_one({'type': 'tables'})['num']
        if in_table_no > table_count:
            raise TableNoError

    def check_table_availability(in_table_no):
        from errors import TableAlreadyOccupiedError
        myc = MW.myc.retaurant_database.orders
        found_table = myc.find_one({'table_no': in_table_no, 'done': False}, {'_id': 1})
        if bool(found_table):
            raise TableAlreadyOccupiedError

    def get_order_no():
        myc = MW.myc.retaurant_database.counter
        order_no = myc.find_one({'type': 'orders'})['num']
        return order_no

    def update_order_counter(count):
        myc = MW.myc.retaurant_database.counter
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.update_one({'type': 'orders'}, {'$set': {'num': count}})
            return True
        except AutoReconnect:
            return False

    def check_customer_in_status(in_phone, in_mail):
        from errors import CustomerAlreadyInError
        myc = MW.myc.retaurant_database.orders
        data_phone = myc.find_one({'phone': in_phone, 'done': False})
        data_mail = myc.find_one({'mail': in_mail, 'done': False})
        if bool(data_phone) or bool(data_mail):
            raise CustomerAlreadyInError

    def create_an_entry_in_orders(in_name, in_table_no, in_phone, in_email):
        order_no = get_order_no()+1
        from datetime import datetime
        data = {
            'name': in_name,
            'order_no': order_no,
            'phone': in_phone,
            'mail': in_email,
            'table_no': in_table_no,
            'foods': [],
            'quantity': [],
            'status_not_taken': [],
            'status_preparing': [],
            'status_prepared': [],
            'total': 0,
            'done': False,
            'in_time': datetime.now(),
            'out_time': datetime.now()
        }
        myc = MW.myc.retaurant_database.orders
        ret_id = myc.insert_one(data)
        from errors import OrderNotCreatedSuccessfullyError
        if not bool(ret_id.inserted_id):
            raise OrderNotCreatedSuccessfullyError

        return order_no

    def revert_an_entry(order_no):
        myc = MW.myc.retaurant_database.orders
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.delete_one({'order_no': order_no})
            MW.mess('Try Again')
        except AutoReconnect:
            revert_an_entry(order_no)

    def update_document(in_name, in_table_no, in_phone, in_mail):
        check_table_counter(int(in_table_no))
        check_table_availability(int(in_table_no))
        check_customer_in_status(in_phone, in_mail)
        new_order_no = create_an_entry_in_orders(in_name, int(in_table_no), in_phone, in_mail)
        completion_status = update_order_counter(new_order_no)
        if not completion_status:
            revert_an_entry(new_order_no)
        MW.logged_user = new_order_no

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

                update_document(in_name, in_table_no, in_phone, in_mail)    # Entering data into database

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
