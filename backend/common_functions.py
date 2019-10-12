def convert_to_bill(doc, amount):
    script = '<style>{}</style>'.format('td, th {padding: 15px;text-align: left;}')
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
    heading = '<h1 text-align="center">{}</h1>'.format('Cyber Restaurant')
    body = '<body>{}{}</body>'.format(heading, table)
    html = '<html>{}{}</html>'.format(script, body)
    return html


def clear_layout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clear_layout(child.layout())