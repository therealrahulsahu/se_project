def run_main_add_food(curr_wid, MW):
    def get_food_id():
        myc = MW.myc.retaurant_database.counter
        food_id = myc.find_one({'type': 'food'})['num']
        return int(food_id)

    def update_food(in_name, in_region, in_type, in_veg, in_price, food_id):
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

    def check_food_availability(in_name):
        from errors import FoodAlreadyAvailableError
        myc = MW.myc.retaurant_database.food
        ret_data = myc.find_one({'name': in_name})
        if bool(ret_data):
            raise FoodAlreadyAvailableError

    def revert_entry_done(in_id):
        myc = MW.myc.retaurant_database.food
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.delete_one({'fid': in_id})
        except AutoReconnect:
            revert_entry_done(in_id)

    def update_food_counter(in_id):
        myc = MW.myc.retaurant_database.counter
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.update_one({'type': 'food'}, {'$set': {'num': in_id}})
        except AutoReconnect:
            revert_entry_done(in_id)

    from PyQt5.QtCore import QThread
    curr_wid.bt_rm_food.setEnabled(False)

    class ThreadAddFood(QThread):

        def __init__(self):
            super().__init__()

        def run(self):
            in_name = curr_wid.le_f_name.text().strip()
            in_region = curr_wid.le_f_region.text().strip()
            in_type = curr_wid.le_f_type.text().strip()
            in_veg = curr_wid.le_f_veg.text().strip()
            in_price = curr_wid.le_price.text().strip()
            from .reg_ex_validation import validFoodName, validRegion, validType, validBool, validPrice
            from errors import InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, \
                InvalidPriceError, FoodAlreadyAvailableError
            from pymongo.errors import AutoReconnect
            try:
                if not validFoodName(in_name):
                    raise InvalidNameError
                if not validRegion(in_region):
                    raise InvalidRegionError
                if not validType(in_type):
                    raise InvalidTypeError
                if not validBool(in_veg):
                    raise InvalidBoolError
                if not validPrice(in_price):
                    raise InvalidPriceError

                if in_veg == 'True':
                    in_veg = True
                else:
                    in_veg = False

                food_id = get_food_id() + 1
                check_food_availability(in_name)
                update_food(in_name, in_region, in_type, in_veg, int(in_price), food_id)
                update_food_counter(int(food_id))

                MW.mess('Food Entry Done')

            except (InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, InvalidPriceError,
                    FoodAlreadyAvailableError) as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_add_food.setEnabled(True)

    class ThreadGetList(QThread):
        def __init__(self):
            super().__init__()
            self.output_list = []

        def run(self):
            in_name = r'{}'.format(curr_wid.le_name_query.text().strip())
            self.output_list = []
            from errors import FoodNotFoundError
            from pymongo.errors import AutoReconnect
            try:
                myc = MW.myc.retaurant_database.food
                data_list = list(myc.find({'name': {'$regex': in_name}},
                                          {'fid': 0, 'available': 0}).limit(10))
                if data_list:
                    curr_wid.cb_rm_food.addItems(
                        ['{0:<20} {1:<5} {2:<5} {3:<5} {4:<5}'.format(x['name'], x['region'], x['type'],
                                                                      str(x['veg']), x['price']) for x in data_list])
                    self.output_list = [x['_id'] for x in data_list]
                    curr_wid.bt_rm_food.setEnabled(True)
                    MW.mess('Food Fetched')
                else:
                    curr_wid.bt_rm_food.setEnabled(False)
                    raise FoodNotFoundError
            except FoodNotFoundError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get.setEnabled(True)

    class ThreadRemoveFood(QThread):
        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            try:
                index = curr_wid.cb_rm_food.currentIndex()
                to_be_delete_id = th_get_food_list.output_list[index]

                myc = MW.myc.retaurant_database.food
                ret_del = myc.delete_one({'_id': to_be_delete_id})
                curr_wid.cb_rm_food.clear()
                MW.mess('Removed')
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get.setEnabled(True)

    th_add_food = ThreadAddFood()
    th_get_food_list = ThreadGetList()
    th_remove_food = ThreadRemoveFood()

    def add_food_thread():
        MW.mess('Adding Food')
        curr_wid.bt_add_food.setEnabled(False)
        th_add_food.start()

    def get_food_list_thread():
        MW.mess('Fetching Food List...')
        curr_wid.cb_rm_food.clear()
        curr_wid.bt_get.setEnabled(False)
        th_get_food_list.start()

    def remove_food_thread():
        curr_wid.bt_rm_food.setEnabled(False)
        curr_wid.bt_get.setEnabled(False)
        MW.mess('Removing...')
        th_remove_food.start()

    curr_wid.bt_add_food.clicked.connect(add_food_thread)
    curr_wid.bt_get.clicked.connect(get_food_list_thread)
    curr_wid.bt_rm_food.clicked.connect(remove_food_thread)