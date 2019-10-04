def check_table_counter(in_table_no, MW):
    from errors import TableNoError
    myc = MW.myc.retaurant_database.counter
    table_count = myc.find_one({'type': 'tables'})['num']
    if in_table_no > table_count:
        raise TableNoError


def check_table_availability(in_table_no, MW):
    from errors import TableAlreadyOccupiedError
    myc = MW.myc.retaurant_database.orders
    found_table = myc.find_one({'table_no': in_table_no, 'done': False}, {'_id': 1})
    if bool(found_table):
        raise TableAlreadyOccupiedError


def get_order_no(MW):
    myc = MW.myc.retaurant_database.counter
    order_no = myc.find_one({'type': 'orders'})['num']
    return order_no


def update_order_counter(count, MW):
    myc = MW.myc.retaurant_database.counter
    from pymongo.errors import AutoReconnect
    try:
        ret_id = myc.update_one({'type': 'orders'}, {'$set': {'num': count}})
        return True
    except AutoReconnect:
        return False


def check_customer_in_status(in_phone, in_mail, MW):
    from errors import CustomerAlreadyInError
    myc = MW.myc.retaurant_database.orders
    data_phone = myc.find_one({'phone': in_phone, 'done': False})
    data_mail = myc.find_one({'mail': in_mail, 'done': False})
    if bool(data_phone) or bool(data_mail):
        raise CustomerAlreadyInError


def create_an_entry_in_orders(in_name, in_table_no, in_phone, in_email, MW):
    order_no = get_order_no(MW) + 1
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


def revert_an_entry(order_no, MW):
    myc = MW.myc.retaurant_database.orders
    from pymongo.errors import AutoReconnect
    try:
        ret_id = myc.delete_one({'order_no': order_no})
        MW.mess('Try Again')
    except AutoReconnect:
        revert_an_entry(order_no, MW)


def update_document(in_name, in_table_no, in_phone, in_mail, MW):
    check_table_counter(int(in_table_no), MW)
    check_table_availability(int(in_table_no), MW)
    check_customer_in_status(in_phone, in_mail, MW)
    new_order_no = create_an_entry_in_orders(in_name, int(in_table_no), in_phone, in_mail, MW)
    completion_status = update_order_counter(new_order_no, MW)
    if not completion_status:
        revert_an_entry(new_order_no, MW)
    MW.logged_user = new_order_no
