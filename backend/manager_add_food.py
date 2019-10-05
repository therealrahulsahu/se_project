def get_food_id(MW):
    myc = MW.myc.retaurant_database.counter
    food_id = myc.find_one({'type': 'food'})['num']
    return int(food_id)


def update_food(in_name, in_region, in_type, in_veg, in_price, food_id, MW):
    myc = MW.myc.retaurant_database.food
    data = {
        'fid': food_id,
        'name': in_name,
        'region': in_region,
        'type': in_type,
        'veg': in_veg,
        'price': in_price,
        'available': True,
    }
    ret_id = myc.insert_one(data)


def check_food_availability(in_name, MW):
    from errors import FoodAlreadyAvailableError
    myc = MW.myc.retaurant_database.food
    ret_data = myc.find_one({'name': in_name})
    if bool(ret_data):
        raise FoodAlreadyAvailableError


def revert_entry_done(in_id, MW):
    myc = MW.myc.retaurant_database.food
    from pymongo.errors import AutoReconnect
    try:
        ret_id = myc.delete_one({'fid': in_id})
    except AutoReconnect:
        revert_entry_done(in_id, MW)


def update_food_counter(in_id, MW):
    myc = MW.myc.retaurant_database.counter
    from pymongo.errors import AutoReconnect
    try:
        ret_id = myc.update_one({'type': 'food'}, {'$set': {'num': in_id}})
    except AutoReconnect:
        revert_entry_done(in_id, MW)
