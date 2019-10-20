from PyQt5.QtWidgets import QMessageBox


def convert_to_bill(doc, data):
    data = dict(data)
    # {'name': 1, 'order_no': 1, 'phone': 1, 'mail': 1, 'table_no': 1,
    # 'foods': 1, 'quantity': 1, 'total': 1, 'in_time': 1, 'out_time': 1}
    customer_info = '<strong>{:>37}</strong>\n' \
                    'Table No. : {:>25}\n' \
                    'Order No. : {:>25}\n' \
                    'Mail      : {:>25}\n' \
                    'Phone     : {:>25}\n' \
                    'Total     : {:>25}\n' \
                    'In Time   : {:>25}\n' \
                    'Out Time  : {:>25}\n'.format(data['name'], data['table_no'], data['order_no'],
                                                  data['mail'], data['phone'], data['total'],
                                                  data['in_time'].strftime('%c'), data['out_time'].strftime('%c'))
    pre = '<pre align="center">{}</pre>'.format(customer_info)
    head_tuple = '<tr><th width="10%">{}</th><th width="40%">{}</th><th width="20%">{}</th>' \
                 '<th width="10%">{}</th><th width="20%">{}</th></tr>'.format('No.', 'Name', 'Price',
                                                                              'Quantity', 'Total')
    data_tuple = ''
    i = 1
    for x in doc:
        data_tuple += '<tr><td width="10%">{}</td><td width="40%">{}</td><td width="20%">{}</td>' \
                 '<td width="10%">{}</td><td width="20%">{}</td></tr>'.format(i, *x)
        i += 1
    data_tuple += '<tr><td colspan="3"><td>Total -> </td><td>{}</td></tr>'.format(data['total'])
    table = '<table width="75%" border="1" align="center">{}{}</table>'.format(head_tuple, data_tuple)
    head_title = '<h1 align="center">{}</h1>'.format('Cyber Restaurant')
    head = '<head>{}</head>'.format('')
    body = '<body>{}{}{}</body>'.format(head_title, pre, table)
    html = '<!DOCTYPE html><html>{}{}</html>'.format(head, body)
    return html


def convert_to_total_sale(data):
    # {'pos': count, 'name': x['name'], 'order_no': x['order_no'],
    # 'time': x['in_time'], 'total': x['total']}
    head_tuple = '<tr><th width="10%">{}</th><th width="30%">{}</th><th width="10%">{}</th>' \
                 '<th width="30%">{}</th><th width="20%">{}</th></tr>'.format('No.', 'Name', 'Order No.',
                                                                              'In Time', 'Total')
    data_tuple = ''
    grand_total = 0
    for x in data:
        data_tuple += '<tr><td width="10%">{}</td><td width="30%">{}</td><td width="10%">{}</td>' \
                      '<td width="30%">{}</td><td width="20%">{}</td></tr>'.format(*x)
        grand_total += x[4]

    data_tuple += '<tr><td colspan="3"></td><td>Grand Total -> </td><td>{}</td></tr>'.format(grand_total)
    table = '<table width="75%" border="1" align="center">{}{}</table>'.format(head_tuple, data_tuple)
    head_title = '<h1 align="center">{}</h1>'.format('Cyber Restaurant')
    head = '<head>{}</head>'.format('')
    body = '<body>{}{}</body>'.format(head_title, table)
    html = '<!DOCTYPE html><html>{}{}</html>'.format(head, body)
    return html


def clear_layout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clear_layout(child.layout())


class DialogConfirmation(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle('Confirm')
        self.setInformativeText(message)
        self.setIcon(QMessageBox.Question)
        from images import ic_milkshake
        self.setWindowIcon(ic_milkshake)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
