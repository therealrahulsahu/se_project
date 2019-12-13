from PyQt5.QtCore import QThread, pyqtSignal


class ThreadAddFood(QThread):

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def set_arg(self, data):
        self.data = data

    def run(self):

        from errors import FoodAlreadyAvailableError
        from pymongo.errors import AutoReconnect
        try:
            food_id = self.get_food_id() + 1
            self.check_food_availability(self.data[0])
            self.update_food(*self.data, food_id)
            self.update_food_counter(int(food_id))

            self.parent_class.MW.mess('Food Entry Done')

        except FoodAlreadyAvailableError as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
        finally:
            self.parent_class.curr_wid.bt_add_food.setEnabled(True)

    def update_food_counter(self, in_id):
        myc = self.parent_class.MW.DB.counter
        from pymongo.errors import AutoReconnect
        try:
            ret_id = myc.update_one({'type': 'food'}, {'$set': {'num': in_id}})
        except AutoReconnect:
            self.parent_class.revert_entry_done(in_id)

    def get_food_id(self):
        myc = self.parent_class.MW.DB.counter
        food_id = myc.find_one({'type': 'food'})['num']
        return int(food_id)

    def update_food(self, in_name, in_region, in_type, in_veg, in_price, food_id):
        myc = self.parent_class.MW.DB.food
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

    def check_food_availability(self, in_name):
        from errors import FoodAlreadyAvailableError
        myc = self.parent_class.MW.DB.food
        ret_data = myc.find_one({'name': in_name})
        if bool(ret_data):
            raise FoodAlreadyAvailableError
