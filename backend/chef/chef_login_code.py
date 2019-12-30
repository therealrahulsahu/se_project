def run_main(curr_wid, MW):
    class Variables:
        def __init__(self):
            pass

    var = Variables()
    var.curr_wid = curr_wid
    var.MW = MW

    from backend.chef.threads.login_code import ThreadLoginChef
    var.fetch_t = ThreadLoginChef(var)

    MW.mess('Enter chef Details ')

    def to_back():
        MW.mess('!!! Select User !!!')
        MW.select_func()

    def to_login():
        MW.mess('Verifying...')
        curr_wid.bt_login.setEnabled(False)
        curr_wid.bt_back.setEnabled(False)
        var.fetch_t.start()

    def to_login_finish():
        MW.logged_user = var.fetch_t.in_userid
        MW.chef_func()

    curr_wid.bt_back.clicked.connect(to_back)
    curr_wid.bt_login.clicked.connect(to_login)
    var.fetch_t.signal.connect(to_login_finish)
