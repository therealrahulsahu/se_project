from PyQt5.QtCore import QThread, pyqtSignal


class ThreadManagerLogin(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def run(self):
        from errors import InvalidPasswordError, InvalidUserIdError, UserNotFoundError
        from backend import RegExValidation
        re_val = RegExValidation()
        from pymongo.errors import AutoReconnect
        self.in_userid = self.parent_class.curr_wid.le_userid.text().strip()
        self.in_password = self.parent_class.curr_wid.le_password.text().strip()
        myc = self.parent_class.MW.DB.manager
        try:
            if not re_val.validUserId(self.in_userid):
                raise InvalidUserIdError
            if not re_val.validPassword(self.in_password):
                raise InvalidPasswordError
            data = myc.find_one({'userid': self.in_userid})
            if not bool(data):
                raise UserNotFoundError
            if data['password'] != self.in_password:
                raise InvalidPasswordError
            self.parent_class.MW.mess('Welcome ' + data['name'])
            self.signal.emit(True)
        except (InvalidUserIdError, InvalidPasswordError, UserNotFoundError) as ob:
            self.parent_class.MW.mess(str(ob))
        except AutoReconnect:
            self.parent_class.MW.mess('--> Network Error <--')
        finally:
            self.parent_class.curr_wid.bt_login.setEnabled(True)
            self.parent_class.curr_wid.bt_back.setEnabled(True)
