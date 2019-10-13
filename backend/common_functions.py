def convert_to_bill(doc, data):
    # TODO: Change Style Sheet and place other data
    data = dict(data)
    # {'name': 1, 'order_no': 1, 'phone': 1, 'mail': 1, 'table_no': 1,
    # 'foods': 1, 'quantity': 1, 'total': 1, 'in_time': 1}
    style = '<style>{}</style>'.format('td, th {width: 25%;}'
                                       'table{width: 50%; border: 1;align: center}'
                                       'h1{align: center}')
    head_tuple = '<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>'.format('No.', 'Name',
                                                                                        'Price', 'Quantity',
                                                                                        'Total')
    data_tuple = ''
    i = 1
    for x in doc:
        data_tuple += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(i, *x)
        i += 1
    data_tuple += '<tr><td></td><td></td><td></td><td>Total -> </td><td>{}</td></tr>'.format(data['total'])
    table = '<table>{}{}</table>'.format(head_tuple, data_tuple)
    head_title = '<h1>{}</h1>'.format('Cyber Restaurant')
    head = '<head>{}</head>'.format(style)
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