def run_main(curr_wid, MW):
    from PyQt5.QtCore import QThread, pyqtSignal

    class ThreadAddFood(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            in_name = curr_wid.le_f_name.text().strip()
            in_region = curr_wid.le_f_region.text().strip()
            in_type = curr_wid.le_f_type.text().strip()
            in_veg = curr_wid.le_f_veg.text().strip()
            in_price = curr_wid.le_price.text().strip()
            from .reg_ex_validation import validName, validRegion, validType, validBool, validPrice
            from errors import InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, \
                InvalidPriceError, FoodAlreadyAvailableError
            from pymongo.errors import AutoReconnect
            try:
                if not validName(in_name):
                    raise InvalidNameError
                if not validRegion(in_region):
                    raise InvalidRegionError
                if not validType(in_type):
                    raise InvalidTypeError
                if not validBool(in_veg):
                    raise InvalidBoolError
                if not validPrice(in_price):
                    raise InvalidPriceError

                from .manager_add_food import get_food_id, check_food_availability, update_food,\
                    update_food_counter
                food_id = get_food_id(MW) + 1
                check_food_availability(in_name, MW)
                update_food(in_name, in_region, in_type, bool(in_veg), int(in_price), food_id, MW)
                update_food_counter(int(food_id), MW)

                MW.mess('Food Entry Done')

            except (InvalidNameError, InvalidRegionError, InvalidTypeError, InvalidBoolError, InvalidPriceError,
                    FoodAlreadyAvailableError) as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_add_food.setEnabled(True)

    th1 = ThreadAddFood()

    def add_food_thread():
        MW.mess('Adding Food')
        curr_wid.bt_add_food.setEnabled(False)
        th1.start()

    curr_wid.bt_add_food.clicked.connect(add_food_thread)
