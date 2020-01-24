def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass

    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.threads import ThreadConnection
    var.th_connection = ThreadConnection(var)

    def connection_line():
        MW.mess('Connecting...')
        link = curr_wid.le_link.text().strip()
        var.th_connection.set_arg(link)
        curr_wid.bt_connect.setEnabled(False)
        var.th_connection.start()

    def connection_file():
        MW.mess('Connecting...')
        try:
            with open('C:\\Users\\KIIT\\Documents\\Cyber_Temp\\connection.txt', 'r') as conn_file:
                link = conn_file.readline().strip()
                curr_wid.le_link.setText(link)
                var.th_connection.set_arg(link)
            curr_wid.bt_connect.setEnabled(False)
            var.th_connection.start()
        except FileNotFoundError:
            MW.mess('Cache Not Found')

    def finish_connection_func():
        MW.mess('Connected')
        with open('C:\\Users\\KIIT\\Documents\\Cyber_Temp\\connection.txt', 'w') as conn_file:
            conn_file.write(var.th_connection.db_link)
        MW.select_func()

    curr_wid.bt_connect.clicked.connect(connection_line)
    var.th_connection.signal.connect(finish_connection_func)
    connection_file()
