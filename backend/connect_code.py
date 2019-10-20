def run_main(curr_wid, MW):
    import dns
    from pymongo.errors import ConfigurationError, ConnectionFailure, ServerSelectionTimeoutError
    from pymongo import MongoClient
    from PyQt5.QtCore import QThread, pyqtSignal
    class ThreadConnection(QThread):

        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):

            try:
                myc = MongoClient('mongodb+srv://therealrahulsahu:rahulsahu1_@'
                                  'democluster-2u6fb.gcp.mongodb.net/test?retryWrites=true',
                                  serverSelectionTimeoutMS=5000, connectTimeoutMS=5000, socketTimeoutMS=5000)
                MW.myc = myc
                MW.DB = eval('myc.{}'.format(MW.current_db))
                from platform import uname
                from datetime import datetime
                login_info_id = MW.DB.se_login_info.insert_one({'info': str(uname()), 'login_time': datetime.now()})
                self.signal.emit(True)
            except (dns.exception.Timeout, ConfigurationError):
                MW.mess('DNS Not Found')
            except ConnectionFailure:
                MW.mess('Connection Failed')
            except ServerSelectionTimeoutError:
                MW.mess('Server Down')
            finally:
                curr_wid.bt_connect.setEnabled(True)

    connection_t = ThreadConnection()

    def conn():
        MW.mess('Connecting...')
        curr_wid.bt_connect.setEnabled(False)
        connection_t.start()

    def conn_finish():
        MW.mess('Connected')
        MW.select_func()

    curr_wid.bt_connect.clicked.connect(conn)
    connection_t.signal.connect(conn_finish)
    conn()
