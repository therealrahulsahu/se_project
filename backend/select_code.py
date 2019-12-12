class RunMain:
    def __init__(self, curr_wid, MW):
        def to_customer():
            MW.customer_login_func()

        def to_manager():
            MW.manager_login_func()

        def to_chef():
            MW.chef_login_func()

        curr_wid.bt_customer.clicked.connect(to_customer)
        curr_wid.bt_manager.clicked.connect(to_manager)
        curr_wid.bt_chef.clicked.connect(to_chef)

def run_main(curr_wid, MW):

    def to_customer():
        MW.customer_login_func()

    def to_manager():
        MW.manager_login_func()

    def to_chef():
        MW.chef_login_func()

    curr_wid.bt_customer.clicked.connect(to_customer)
    curr_wid.bt_manager.clicked.connect(to_manager)
    curr_wid.bt_chef.clicked.connect(to_chef)
