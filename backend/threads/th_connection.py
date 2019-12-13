from PyQt5.QtCore import QThread, pyqtSignal


class ThreadConnection(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.db_user_id = ''
        self.db_password = ''
        self.parent_class = parent_class

    def set_arg(self, db_link):
        self.db_link = db_link

    def run(self):
        import dns
        from pymongo.errors import ConfigurationError, ConnectionFailure, \
            ServerSelectionTimeoutError, OperationFailure
        from pymongo import MongoClient
        try:
            myc = MongoClient('{}'.format(self.db_link),
                              serverSelectionTimeoutMS=5000, connectTimeoutMS=5000, socketTimeoutMS=5000)
            self.parent_class.MW.myc = myc
            self.parent_class.MW.DB = eval('myc.{}'.format(self.parent_class.MW.current_db))
            from platform import uname, node
            from datetime import datetime
            login_info_id = self.parent_class.MW.DB.se_login_info.insert_one({'info': str(uname()),
                                                                               'name': str(node()),
                                                                               'login_time': datetime.now()})
            self.signal.emit(True)
        except (dns.exception.Timeout, ConfigurationError):
            self.parent_class.MW.mess('DNS Not Found')
        except ConnectionFailure:
            self.parent_class.MW.mess('-->>Network Error<<--')
        except ServerSelectionTimeoutError:
            self.parent_class.MW.mess('Server Down')
        except OperationFailure:
            self.parent_class.MW.mess('Wrong Database Id/Password')
        finally:
            self.parent_class.curr_wid.bt_connect.setEnabled(True)
