class RunMain:
    def __init__(self, curr_wid, MW):
        MW.mess('Enter Manager Details ')

        def to_back():
            MW.mess('!!! Select User !!!')
            MW.select_func()

        curr_wid.bt_back.clicked.connect(to_back)

        from PyQt5.QtCore import QThread, pyqtSignal

        class ThreadFetch(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                super().__init__()

            def run(self):
                from errors import InvalidPasswordError, InvalidUserIdError, UserNotFoundError
                from .reg_ex_validation import validUserId, validPassword
                from pymongo.errors import AutoReconnect
                self.in_userid = curr_wid.le_userid.text().strip()
                self.in_password = curr_wid.le_password.text().strip()
                myc = MW.DB.manager
                try:
                    if not validUserId(self.in_userid):
                        raise InvalidUserIdError
                    if not validPassword(self.in_password):
                        raise InvalidPasswordError
                    data = myc.find_one({'userid': self.in_userid})
                    if not bool(data):
                        raise UserNotFoundError
                    if data['password'] != self.in_password:
                        raise InvalidPasswordError
                    MW.mess('Welcome ' + data['name'])
                    self.signal.emit(True)
                except (InvalidUserIdError, InvalidPasswordError, UserNotFoundError) as ob:
                    MW.mess(str(ob))
                except AutoReconnect:
                    MW.mess('--> Network Error <--')
                finally:
                    curr_wid.bt_login.setEnabled(True)
                    curr_wid.bt_back.setEnabled(True)

        fetch_t = ThreadFetch()

        def to_login():
            MW.mess('Verifying...')
            curr_wid.bt_login.setEnabled(False)
            curr_wid.bt_back.setEnabled(False)
            fetch_t.start()

        def to_login_finish():
            MW.logged_user = fetch_t.in_userid
            MW.manager_func()

        curr_wid.bt_login.clicked.connect(to_login)
        fetch_t.signal.connect(to_login_finish)

def run_main(curr_wid, MW):
    MW.mess('Enter Manager Details ')

    def to_back():
        MW.mess('!!! Select User !!!')
        MW.select_func()

    curr_wid.bt_back.clicked.connect(to_back)

    from PyQt5.QtCore import QThread, pyqtSignal

    class ThreadFetch(QThread):
        signal = pyqtSignal('PyQt_PyObject')

        def __init__(self):
            super().__init__()

        def run(self):
            from errors import InvalidPasswordError, InvalidUserIdError, UserNotFoundError
            from .reg_ex_validation import validUserId, validPassword
            from pymongo.errors import AutoReconnect
            self.in_userid = curr_wid.le_userid.text().strip()
            self.in_password = curr_wid.le_password.text().strip()
            myc = MW.DB.manager
            try:
                if not validUserId(self.in_userid):
                    raise InvalidUserIdError
                if not validPassword(self.in_password):
                    raise InvalidPasswordError
                data = myc.find_one({'userid': self.in_userid})
                if not bool(data):
                    raise UserNotFoundError
                if data['password'] != self.in_password:
                    raise InvalidPasswordError
                MW.mess('Welcome ' + data['name'])
                self.signal.emit(True)
            except (InvalidUserIdError, InvalidPasswordError, UserNotFoundError) as ob:
                MW.mess(str(ob))
            except AutoReconnect:
                MW.mess('--> Network Error <--')
            finally:
                curr_wid.bt_login.setEnabled(True)
                curr_wid.bt_back.setEnabled(True)

    fetch_t = ThreadFetch()

    def to_login():
        MW.mess('Verifying...')
        curr_wid.bt_login.setEnabled(False)
        curr_wid.bt_back.setEnabled(False)
        fetch_t.start()

    def to_login_finish():
        MW.logged_user = fetch_t.in_userid
        MW.manager_func()

    curr_wid.bt_login.clicked.connect(to_login)
    fetch_t.signal.connect(to_login_finish)
