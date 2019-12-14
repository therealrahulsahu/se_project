from PyQt5.QtCore import QThread, pyqtSignal


class ThreadPreparationRefresh(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        from errors import NoOrdersFoundError
        from pymongo.errors import AutoReconnect
        try:
            query_ret = {
                '_id': 1,
                'table_no': 1,
                'foods': 1,
                'status_not_taken': 1,
                'status_preparing': 1
            }
            ret_customers = self.parent_class.myc_o.find({'done': False}, query_ret)
            for cus_dict in ret_customers:
                cus_data = zip(cus_dict['foods'], cus_dict['status_not_taken'],
                               cus_dict['status_preparing'])
                for food_tuple in cus_data:
                    food_name = self.parent_class.myc_f.find_one({'_id': food_tuple[0]}, {'name': 1})['name']
                    if food_tuple[1]:
                        self.parent_class.request_widget_list.append(
                            (cus_dict['_id'], food_tuple[0], food_name,
                             food_tuple[1], cus_dict['table_no']))
                    if food_tuple[2]:
                        self.parent_class.preparation_widget_list.append(
                            (cus_dict['_id'], food_tuple[0], food_name,
                             food_tuple[2], cus_dict['table_no']))

            self.signal.emit(True)
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error<<--')
        except NoOrdersFoundError as ob:
            self.parent_class.MW.mess(str(ob))
        finally:
            self.parent_class.curr_wid.bt_refresh.setEnabled(True)
