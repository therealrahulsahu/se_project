class RunMainLogin:
    def __init__(self, curr_wid, MW):
        self.curr_wid = curr_wid
        self.MW = MW

        MW.mess('Enter Manager Details ')

        self.curr_wid.bt_back.clicked.connect(self.to_back)

        from backend.manager.threads.login_code import ThreadManagerLogin
        self.fetch_t = ThreadManagerLogin(self)

        self.curr_wid.bt_login.clicked.connect(self.to_login)
        self.fetch_t.signal.connect(self.to_login_finish)

    def to_back(self):
        self.MW.mess('!!! Select User !!!')
        self.MW.select_func()

    def to_login(self):
        self.MW.mess('Verifying...')
        self.curr_wid.bt_login.setEnabled(False)
        self.curr_wid.bt_back.setEnabled(False)
        self.fetch_t.start()

    def to_login_finish(self):
        self.MW.logged_user = self.fetch_t.in_userid
        self.MW.manager_func()
