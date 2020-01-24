from PyQt5.QtCore import QThread, pyqtSignal


class ThreadConnection(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.db_link = ''
        self.parent_class = parent_class

    def set_arg(self, link):
        self.db_link = link

    def run(self):
        import dns
        from pymongo.errors import ConfigurationError, ConnectionFailure, \
            ServerSelectionTimeoutError, OperationFailure
        from pymongo import MongoClient
        try:
            myc = MongoClient(self.db_link, serverSelectionTimeoutMS=5000,
                              connectTimeoutMS=5000, socketTimeoutMS=5000)
            self.parent_class.MW.myc = myc
            self.parent_class.MW.DB = eval('myc.{}'.format(self.parent_class.MW.current_db))

            manager_found = self.parent_class.MW.DB.manager.find_one({})
            if not bool(manager_found):
                if self.db_link == 'mongodb://localhost:27017/':
                    user_name = 'localhost'
                    user_password = 'localhost'
                else:
                    from re import compile
                    reg = compile(r'(?i)(?<=\/\/)(\w+)(:)(\w+)(?=@)')
                    data = reg.search(self.db_link)
                    user_name = data.group(1)
                    user_password = data.group(3)
                in_id1 = self.parent_class.MW.DB.manager.insert_one({'name': user_name,
                                                                     'userid': user_name,
                                                                     'password': user_password})
                in_id2 = self.parent_class.MW.DB.counter.insert_many([{'type': 'food', 'num': 0},
                                                                      {'type': 'orders', 'num': 0},
                                                                      {'type': 'tables', 'num': 10}])

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
