class RunMainChangeFoodAva:
    def __init__(self, curr_wid, MW):
        from PyQt5.QtCore import QThread, pyqtSignal

        class ThreadGetFoodList(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()
                self.output = []

            def run(self):
                in_name = '(?i)' + curr_wid.le_food_name.text().strip()
                from errors import FoodNotFoundError
                from pymongo.errors import AutoReconnect
                try:
                    myc = MW.DB.food
                    data_list = list(
                        myc.find({'name': {'$regex': in_name}}, {'_id': 1, 'name': 1, 'available': 1}).limit(10))
                    if data_list:
                        self.output = data_list
                        self.signal.emit(True)
                    else:
                        raise FoodNotFoundError
                except FoodNotFoundError as ob:
                    MW.mess(str(ob))
                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                finally:
                    curr_wid.bt_get_food.setEnabled(True)

        class ThreadMarkAva(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()

            def run(self):
                index = curr_wid.cb_food_list.currentIndex()
                to_update_id = th_get_food_list.output[index]['_id']
                from pymongo.errors import AutoReconnect
                try:
                    myc = MW.DB.food
                    ret_id = myc.update_one({'_id': to_update_id}, {'$set': {'available': True}})
                    MW.mess('Marked')
                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                finally:
                    curr_wid.bt_get_food.setEnabled(True)

        class ThreadMarkUnAva(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()

            def run(self):
                index = curr_wid.cb_food_list.currentIndex()
                to_update_id = th_get_food_list.output[index]['_id']
                from pymongo.errors import AutoReconnect
                try:
                    myc = MW.DB.food
                    ret_id = myc.update_one({'_id': to_update_id}, {'$set': {'available': False}})
                    MW.mess('Marked')
                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->> Network Error <<--')
                finally:
                    curr_wid.bt_get_food.setEnabled(True)

        th_get_food_list = ThreadGetFoodList()
        th_mark_ava = ThreadMarkAva()
        th_mark_un_ava = ThreadMarkUnAva()

        curr_wid.bt_mark_ava.setEnabled(False)
        curr_wid.bt_mark_un_ava.setEnabled(False)

        def get_food_thread():
            MW.mess('Fetching List...')
            curr_wid.cb_food_list.clear()
            curr_wid.bt_get_food.setEnabled(False)
            th_get_food_list.start()

        def finish_get_food_thread():
            to_be_add = ['{}{}{}'.format(x['name'], ' ' * 10, bool(x['available'])) for x in th_get_food_list.output]
            curr_wid.cb_food_list.addItems(to_be_add)
            MW.mess('Food Fetched')
            curr_wid.bt_mark_ava.setEnabled(True)
            curr_wid.bt_mark_un_ava.setEnabled(True)

        def mark_food_ava():
            MW.mess('Marking Unavailable')
            curr_wid.bt_get_food.setEnabled(False)
            curr_wid.bt_mark_ava.setEnabled(False)
            curr_wid.bt_mark_un_ava.setEnabled(False)
            th_mark_ava.start()

        def finish_mark_food_ava():
            curr_wid.cb_food_list.clear()

        def mark_food_un_ava():
            MW.mess('Mark Available')
            curr_wid.bt_get_food.setEnabled(False)
            curr_wid.bt_mark_ava.setEnabled(False)
            curr_wid.bt_mark_un_ava.setEnabled(False)
            th_mark_un_ava.start()

        curr_wid.bt_get_food.clicked.connect(get_food_thread)
        th_get_food_list.signal.connect(finish_get_food_thread)

        curr_wid.bt_mark_ava.clicked.connect(mark_food_ava)
        th_mark_ava.signal.connect(finish_mark_food_ava)
        th_mark_un_ava.signal.connect(finish_mark_food_ava)

        curr_wid.bt_mark_un_ava.clicked.connect(mark_food_un_ava)


def run_main_change_food_ava(curr_wid, MW):
    from PyQt5.QtCore import QThread, pyqtSignal

    class ThreadGetFoodList(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.output = []

        def run(self):
            in_name = '(?i)' + curr_wid.le_food_name.text().strip()
            from errors import FoodNotFoundError
            from pymongo.errors import AutoReconnect
            try:
                myc = MW.DB.food
                data_list = list(myc.find({'name': {'$regex': in_name}}, {'_id': 1, 'name': 1, 'available': 1}).limit(10))
                if data_list:
                    self.output = data_list
                    self.signal.emit(True)
                else:
                    raise FoodNotFoundError
            except FoodNotFoundError as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get_food.setEnabled(True)

    class ThreadMarkAva(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            index = curr_wid.cb_food_list.currentIndex()
            to_update_id = th_get_food_list.output[index]['_id']
            from pymongo.errors import AutoReconnect
            try:
                myc = MW.DB.food
                ret_id = myc.update_one({'_id': to_update_id}, {'$set': {'available': True}})
                MW.mess('Marked')
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get_food.setEnabled(True)

    class ThreadMarkUnAva(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            index = curr_wid.cb_food_list.currentIndex()
            to_update_id = th_get_food_list.output[index]['_id']
            from pymongo.errors import AutoReconnect
            try:
                myc = MW.DB.food
                ret_id = myc.update_one({'_id': to_update_id}, {'$set': {'available': False}})
                MW.mess('Marked')
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            finally:
                curr_wid.bt_get_food.setEnabled(True)

    th_get_food_list = ThreadGetFoodList()
    th_mark_ava = ThreadMarkAva()
    th_mark_un_ava = ThreadMarkUnAva()

    curr_wid.bt_mark_ava.setEnabled(False)
    curr_wid.bt_mark_un_ava.setEnabled(False)

    def get_food_thread():
        MW.mess('Fetching List...')
        curr_wid.cb_food_list.clear()
        curr_wid.bt_get_food.setEnabled(False)
        th_get_food_list.start()

    def finish_get_food_thread():
        to_be_add = ['{}{}{}'.format(x['name'], ' ' * 10, bool(x['available'])) for x in th_get_food_list.output]
        curr_wid.cb_food_list.addItems(to_be_add)
        MW.mess('Food Fetched')
        curr_wid.bt_mark_ava.setEnabled(True)
        curr_wid.bt_mark_un_ava.setEnabled(True)

    def mark_food_ava():
        MW.mess('Marking Unavailable')
        curr_wid.bt_get_food.setEnabled(False)
        curr_wid.bt_mark_ava.setEnabled(False)
        curr_wid.bt_mark_un_ava.setEnabled(False)
        th_mark_ava.start()

    def finish_mark_food_ava():
        curr_wid.cb_food_list.clear()

    def mark_food_un_ava():
        MW.mess('Mark Available')
        curr_wid.bt_get_food.setEnabled(False)
        curr_wid.bt_mark_ava.setEnabled(False)
        curr_wid.bt_mark_un_ava.setEnabled(False)
        th_mark_un_ava.start()

    curr_wid.bt_get_food.clicked.connect(get_food_thread)
    th_get_food_list.signal.connect(finish_get_food_thread)

    curr_wid.bt_mark_ava.clicked.connect(mark_food_ava)
    th_mark_ava.signal.connect(finish_mark_food_ava)
    th_mark_un_ava.signal.connect(finish_mark_food_ava)

    curr_wid.bt_mark_un_ava.clicked.connect(mark_food_un_ava)
