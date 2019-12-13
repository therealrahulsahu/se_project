from PyQt5.QtCore import QThread, pyqtSignal


class ThreadCreateCustomer(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def set_arg(self, data):
        self.data = data

    def run(self):

        from errors import CustomerAlreadyInError, TableAlreadyOccupiedError, OrderNotCreatedSuccessfullyError
        from pymongo.errors import AutoReconnect

        try:
            self.update_document(*self.data)  # Entering data into database

            self.parent_class.MW.mess('Welcome : ' + self.data[0])
            self.signal.emit(True)

        except (TableAlreadyOccupiedError, OrderNotCreatedSuccessfullyError) as ob:
            self.parent_class.MW.mess(str(ob))
        except CustomerAlreadyInError as ob:
            self.parent_class.MW.mess(str(ob))
            self.parent_class.MW.logged_user = ob.customer_id
            self.parent_class.MW.mess('Welcome Back: ' + ob.name)
            self.signal.emit(True)

        except AutoReconnect:
            self.parent_class.MW.mess('--> Network Error <--')
        finally:
            self.parent_class.curr_wid.bt_get_started.setEnabled(True)
            self.parent_class.curr_wid.bt_back.setEnabled(True)

    def check_table_counter(self, in_table_no):
        from errors import TableNoError
        myc = self.parent_class.MW.DB.counter
        table_count = myc.find_one({'type': 'tables'})['num']
        if in_table_no > table_count:
            raise TableNoError

    def check_table_availability(self, in_table_no):
        from errors import TableAlreadyOccupiedError
        myc = self.parent_class.MW.DB.orders
        found_table = myc.find_one({'table_no': in_table_no, 'pay_done': False}, {'_id': 1})
        if bool(found_table):
            raise TableAlreadyOccupiedError

    def get_order_no(self):
        myc = self.parent_class.MW.DB.counter
        order_no = myc.find_one({'type': 'orders'})['num']
        return order_no

    def update_order_counter(self, count):
        myc = self.parent_class.MW.DB.counter
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.update_one({'type': 'orders'}, {'$set': {'num': count}})
            return True
        except AutoReconnect:
            return False

    def check_customer_in_status(self, in_phone, in_mail):
        from errors import CustomerAlreadyInError
        myc = self.parent_class.MW.DB.orders
        data_phone = myc.find_one({'phone': in_phone, 'done': False})
        if bool(data_phone):
            raise CustomerAlreadyInError(data_phone['_id'], data_phone['name'])

    def create_an_entry_in_orders(self, in_name, in_table_no, in_phone, in_email):
        order_no = self.get_order_no() + 1
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
            'pay_done': False,
            'done': False,
            'in_time': datetime.now(),
            'out_time': datetime.now()
        }
        myc = self.parent_class.MW.DB.orders
        ret_id = myc.insert_one(data)
        self.parent_class.MW.logged_user = ret_id.inserted_id  # Object id inserted
        from errors import OrderNotCreatedSuccessfullyError
        if not bool(ret_id.inserted_id):
            raise OrderNotCreatedSuccessfullyError

        return order_no

    def revert_an_entry(self, order_no):
        myc = self.parent_class.MW.DB.orders
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.delete_one({'order_no': order_no})
            self.parent_class.MW.mess('Try Again')
        except AutoReconnect:
            self.revert_an_entry(order_no)

    def update_document(self, in_name, in_table_no, in_phone, in_mail):
        self.check_table_counter(int(in_table_no))
        self.check_customer_in_status(in_phone, in_mail)
        self.check_table_availability(int(in_table_no))
        new_order_no = self.create_an_entry_in_orders(in_name, int(in_table_no), in_phone, in_mail)
        completion_status = self.update_order_counter(new_order_no)
        if not completion_status:
            self.revert_an_entry(new_order_no)
