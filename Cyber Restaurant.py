from PyQt5.QtWidgets import QMainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(640, 360)
        self.setWindowTitle('Cyber Restaurant')
        from images import ic_milkshake
        self.setWindowIcon(ic_milkshake)
        self.logged_user = ''
        self.current_db = 'retaurant_database'

        self.bar_menu = self.menuBar()
        self.menu_bar()

        self.bar_status = self.statusBar()
        self.status_bar()

        self.start_here()

    def global_style(self, AW):

        self.AW = AW

        from PyQt5.QtGui import QFont
        my_font = QFont('Comic Sans MS')
        my_font.setPointSize(8)
        self.AW.setFont(my_font)

        import qdarkstyle
        # from backend import orange_s_sheet
        # self.AW.setStyleSheet(orange_s_sheet)
        self.AW.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def menu_bar(self):

        from PyQt5.QtWidgets import QAction
        quit_action = QAction('&Quit Session', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Quit Session')
        quit_action.triggered.connect(self.select_func)

        file_menu = self.bar_menu.addMenu('&File')
        file_menu.addAction(quit_action)

    def status_bar(self):
        self.mess = self.bar_status.showMessage
        self.mess('Ready to Go....')

    def select_func(self):
        self.bar_menu.setVisible(False)
        self.logged_user = ''

        from PyQt5.QtWidgets import QWidget
        select_wid = QWidget()
        from frontend import SelectWid
        select_ui = SelectWid()
        select_ui.setupUi(select_wid)
        from backend import SelectCode
        SelectCode(select_ui, self)

        self.setCentralWidget(select_wid)

    def customer_login_func(self):
        self.bar_menu.setVisible(False)

        from PyQt5.QtWidgets import QWidget
        customer_login_wid = QWidget()
        from frontend import CustomerLoginWid
        customer_login_ui = CustomerLoginWid()
        customer_login_ui.setupUi(customer_login_wid)
        from backend import CustomerLoginCode
        CustomerLoginCode(customer_login_ui, self)

        self.setCentralWidget(customer_login_wid)

    def manager_login_func(self):
        self.bar_menu.setVisible(False)

        from PyQt5.QtWidgets import QWidget
        manager_login_wid = QWidget()
        from frontend import ManagerLoginWid
        manager_login_ui = ManagerLoginWid()
        manager_login_ui.setupUi(manager_login_wid)
        from backend import ManagerLoginCode
        ManagerLoginCode(manager_login_ui, self)

        self.setCentralWidget(manager_login_wid)

    def chef_login_func(self):
        self.bar_menu.setVisible(False)

        from PyQt5.QtWidgets import QWidget
        chef_login_wid = QWidget()
        from frontend import ChefLoginWid
        chef_login_ui = ChefLoginWid()
        chef_login_ui.setupUi(chef_login_wid)
        from backend import ChefLoginCode
        ChefLoginCode(chef_login_ui, self)

        self.setCentralWidget(chef_login_wid)

    def connect_func(self):
        self.bar_menu.setVisible(False)

        from PyQt5.QtWidgets import QWidget
        conn_wid = QWidget()
        from frontend import ConnectWid
        conn_ui = ConnectWid()
        conn_ui.setupUi(conn_wid)
        from backend import ConnectCode
        ConnectCode(conn_ui, self)

        self.setCentralWidget(conn_wid)

    def manager_func(self):
        self.bar_menu.setVisible(True)

        from PyQt5.QtWidgets import QWidget
        manager_wid = QWidget()
        from frontend import ManagerWid
        manager_ui = ManagerWid()
        manager_ui.setupUi(manager_wid)
        from backend import ManagerCode
        ManagerCode(manager_ui, self)

        self.setCentralWidget(manager_wid)

    def chef_func(self):
        self.bar_menu.setVisible(True)

        from PyQt5.QtWidgets import QWidget
        chef_wid = QWidget()
        from frontend import ChefWid
        chef_ui = ChefWid()
        chef_ui.setupUi(chef_wid)
        from backend import ChefCode
        ChefCode(chef_ui, self)

        self.setCentralWidget(chef_wid)

    def customer_func(self):
        self.bar_menu.setVisible(True)

        from PyQt5.QtWidgets import QWidget
        customer_wid = QWidget()
        from frontend import CustomerWid
        customer_ui = CustomerWid()
        customer_ui.setupUi(customer_wid)
        from backend import CustomerCode
        CustomerCode(customer_ui, self)

        self.setCentralWidget(customer_wid)

    def start_here(self):
        self.connect_func()

    def closeEvent(self, event):
        from PyQt5.QtWidgets import QMessageBox
        from images import ic_milkshake
        box = QMessageBox()
        box.setWindowIcon(ic_milkshake)
        box.resize(200, 100)
        if self.logged_user:
            box.setWindowTitle('!!! Action Denied !!!')
            box.setInformativeText('Please\nComplete Order.\nOR\nLogout.')
            box.setIcon(QMessageBox.Warning)
            box.setStandardButtons(QMessageBox.Ok)
            response = box.exec_()
            if response == QMessageBox.Ok:
                event.ignore()
        else:
            box.setWindowTitle('Confirm...')
            box.setInformativeText('Are You Sure ?')
            box.setIcon(QMessageBox.Question)
            box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            response = box.exec_()
            if response == QMessageBox.Ok:
                event.accept()
            elif response == QMessageBox.Cancel:
                event.ignore()


if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication
    import sys
    AW = QApplication(sys.argv)
    win = MyWindow()
    win.global_style(AW)
    win.show()

    end = AW.exec_()
    if not end:
        try:
            win.myc.close()
        except AttributeError:
            pass
        sys.exit(end)

# todo : auto refresh to be done in tab widgets
# todo : Frame less window
