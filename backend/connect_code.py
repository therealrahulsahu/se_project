def run_main(curr_wid, MW):
    import dns
    from pymongo.errors import ConfigurationError, ConnectionFailure, \
        ServerSelectionTimeoutError, OperationFailure
    from pymongo import MongoClient
    from PyQt5.QtCore import QThread, pyqtSignal
    class ThreadConnection(QThread):

        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()
            self.db_user_id = ''
            self.db_password = ''

        def set_arg(self, db_user_id, db_password):
            self.db_user_id = db_user_id
            self.db_password = db_password

        def run(self):

            try:
                myc = MongoClient('mongodb+srv://{}:{}democluster-2u6fb.gcp.'
                                  'mongodb.net/test?retryWrites=true'.format(self.db_user_id, self.db_password),
                                  serverSelectionTimeoutMS=5000, connectTimeoutMS=5000, socketTimeoutMS=5000)
                MW.myc = myc
                MW.DB = eval('myc.{}'.format(MW.current_db))
                from platform import uname, node
                from datetime import datetime
                login_info_id = MW.DB.se_login_info.insert_one({'info': str(uname()),
                                                                'name': str(node()),
                                                                'login_time': datetime.now()})
                self.signal.emit(True)
            except (dns.exception.Timeout, ConfigurationError):
                MW.mess('DNS Not Found')
            except ConnectionFailure:
                MW.mess('-->>Network Error<<--')
            except ServerSelectionTimeoutError:
                MW.mess('Server Down')
            except OperationFailure:
                MW.mess('Wrong Database Id/Password')
            finally:
                curr_wid.bt_connect.setEnabled(True)

    th_connection = ThreadConnection()

    def connection_func():
        MW.mess('Connecting...')
        from .connection_details import mongodb_user_id, mongodb_password
        th_connection.set_arg(mongodb_user_id, mongodb_password)
        curr_wid.bt_connect.setEnabled(False)
        th_connection.start()

    def finish_connection_func():
        MW.mess('Connected')
        MW.select_func()

    curr_wid.bt_connect.clicked.connect(connection_func)
    th_connection.signal.connect(finish_connection_func)
    connection_func()
