def run_main_bill(curr_wid, MW):
    customer_id = MW.logged_user
    from PyQt5.QtCore import QThread, pyqtSignal

    def convert_to_bill(doc, amount):
        script = '<style>{}</style>'.format('td, th {padding: 10px;text-align: left;}')
        heading = '<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>'.format('No.', 'Name',
                                                                                            'Price', 'Quantity',
                                                                                            'Total')
        data_tuple = ''
        i = 1
        for x in doc:
            data_tuple += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(i, *x)
            i += 1
        data_tuple += '<tr><td></td><td></td><td></td><td>Total -> </td><td>{}</td></tr>'.format(amount)
        table = '<table border="1">{}{}</table>'.format(heading, data_tuple)
        body = '<body>{}</body>'.format(table)
        html = '<html>{}{}</html>'.format(script, body)
        return html

    class ThreadRefreshBill(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.bill_doc = []
            self.total_bill = 0

        def run(self):
            self.bill_doc = []
            self.total_bill = 0
            from pymongo.errors import AutoReconnect
            from errors import NoOrdersFoundError
            try:
                myc_o = MW.DB.orders
                myc_f = MW.DB.food
                order_data = myc_o.find_one({'_id': customer_id}, {'foods': 1, 'quantity': 1, 'total': 1})
                self.total_bill = order_data['total']
                order_data = list(zip(order_data['foods'], order_data['quantity']))
                for x in order_data:
                    food_detail = myc_f.find_one({'_id': x[0]}, {'name': 1, 'price': 1})
                    self.bill_doc.append([food_detail['name'], food_detail['price'], x[1], food_detail['price'] * x[1]])
                self.signal.emit(True)
            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            except NoOrdersFoundError as ob:
                MW.mess(str(ob))
            finally:
                curr_wid.bt_refresh_bill.setEnabled(True)

    th_refresh_bill = ThreadRefreshBill()

    def refresh_bill_func():
        curr_wid.bt_refresh_bill.setEnabled(False)
        curr_wid.tb_bill.setText('')
        MW.mess('Refreshing...')
        th_refresh_bill.start()

    def finish_refresh_bill_func():
        curr_wid.tb_bill.setText(convert_to_bill(th_refresh_bill.bill_doc, th_refresh_bill.total_bill))
        MW.mess('Refreshed')

    curr_wid.bt_refresh_bill.clicked.connect(refresh_bill_func)
    th_refresh_bill.signal.connect(finish_refresh_bill_func)
    # refresh_bill_func()

    class ThreadCheckout(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            from pymongo.errors import AutoReconnect
            from errors import SomeOrdersPreparingError, NoOrdersFoundError
            myc_o = MW.DB.orders
            try:
                order = myc_o.find_one({'_id': customer_id}, {'quantity': 1, 'status_not_taken': 1, 'done': 1})
                if any(order['status_not_taken']):
                    raise SomeOrdersPreparingError
                elif not len(order['quantity']):
                    raise NoOrdersFoundError
                else:
                    order['done'] = True
                    ret_id = myc_o.update_one({'_id': customer_id}, {'$set': order})
                    self.signal.emit(True)

            except AutoReconnect:
                MW.mess('-->> Network Error <<--')
            except (SomeOrdersPreparingError, NoOrdersFoundError) as ob:
                MW.mess(str(ob))
            finally:
                curr_wid.bt_checkout.setEnabled(True)

    th_checkout = ThreadCheckout()

    def checkout_func():
        curr_wid.bt_checkout.setEnabled(False)
        MW.mess('Finishing...')
        th_checkout.start()

    def finish_checkout():
        MW.mess('Thank You {}(  Your Bill {}  )'.format(' '*15, th_refresh_bill.total_bill))
        MW.select_func()

    curr_wid.bt_checkout.clicked.connect(checkout_func)
    th_checkout.signal.connect(finish_checkout)

