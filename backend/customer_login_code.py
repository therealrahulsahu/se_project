def run_main(curr_wid, MW):
    def to_back():
        MW.mess('!!! Select User !!!')
        MW.select_func()

    curr_wid.bt_back.clicked.connect(to_back)
