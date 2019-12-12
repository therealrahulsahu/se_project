class RunMainRestaurant:
    def __init__(self, curr_wid, MW):
        from PyQt5.QtCore import QThread, pyqtSignal

        class ThreadGetTableNo(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()
                self.output = 0

            def run(self):
                from pymongo.errors import AutoReconnect
                try:
                    rev_data = MW.DB.counter.find_one({'type': 'tables'})
                    self.output = rev_data['num']
                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->>Network<<--Error')
                finally:
                    curr_wid.bt_change.setEnabled(True)

        th_get_table_no = ThreadGetTableNo()

        def get_table_no_func():
            MW.mess('Fetching...')
            curr_wid.bt_change.setEnabled(False)
            th_get_table_no.start()

        def finish_get_table_no_func():
            MW.mess('Fetched')
            curr_wid.lb_table_no_2.setText(str(th_get_table_no.output))
            curr_wid.le_table_no.setText(str(th_get_table_no.output))

        th_get_table_no.signal.connect(finish_get_table_no_func)
        get_table_no_func()

        def change_quantity():
            try:
                val = int(curr_wid.le_table_no.text().strip())
                if 0 < val < 100:
                    MW.mess('Quantity Changed')
                else:
                    raise ValueError
            except ValueError:
                MW.mess('Invalid Quantity')
                curr_wid.le_table_no.setText(str(th_get_table_no.output))

        curr_wid.le_table_no.editingFinished.connect(change_quantity)

        class ThreadChangeTableNo(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()
                self.num = 0

            def set_arg(self, num):
                self.num = num

            def run(self):
                from pymongo.errors import AutoReconnect
                try:
                    rev_ids = MW.DB.counter.update_one({'type': 'tables'}, {'$set': {'num': self.num}})
                    self.signal.emit(True)
                except AutoReconnect:
                    MW.mess('-->>Network Error<<--')
                finally:
                    curr_wid.bt_change.setEnabled(True)

        th_change_table_no = ThreadChangeTableNo()

        def change_table_no_func():
            MW.mess('Changing...')
            curr_wid.bt_change.setEnabled(False)
            th_change_table_no.set_arg(int(curr_wid.le_table_no.text().strip()))
            th_change_table_no.start()

        def finish_change_table_no_func():
            MW.mess('Changed')
            get_table_no_func()

        curr_wid.bt_change.clicked.connect(change_table_no_func)
        th_change_table_no.signal.connect(finish_change_table_no_func)
