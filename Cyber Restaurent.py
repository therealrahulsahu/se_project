from PyQt5 import QtWidgets
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(640, 360)
        self.setWindowTitle('Cyber Restaurant')
        # self.setWindowIcon(ic_insert_table)
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

        qpushbutton = """
            QPushButton
            {
                background-color: pink;
                border: 1px solid blue;
                width: 60px;
                height: 15px;
                color: red;
            }
        """
        qlineedit = """
            QLineEdit
            {
                background-color: pink;
                border: 1px solid black;
                color: red;
            }
        """
        qlabel = """
            QLabel
            {
                color: red;
            }
        """
        qmainwindow = """
            QMainWindow
            {
                background-color: orange;
            }
        """
        qwidget = """
            QWidget
            {
                background-color: yellow;
            }
        """

        my_css = qpushbutton + qlineedit + qlabel + qmainwindow
        self.AW.setStyleSheet(my_css)

    def menu_bar(self):

        quit_action = QtWidgets.QAction('&Quit Session', self)
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

        select_wid = QtWidgets.QWidget()
        from frontend import SelectWid
        select_ui = SelectWid()
        select_ui.setupUi(select_wid)
        from backend import SelectCode
        SelectCode(select_ui, self)

        self.setCentralWidget(select_wid)

    def customer_login_func(self):
        self.bar_menu.setVisible(False)

        customer_login_wid = QtWidgets.QWidget()
        from frontend import CustomerLoginWid
        customer_login_ui = CustomerLoginWid()
        customer_login_ui.setupUi(customer_login_wid)
        from backend import CustomerLoginCode
        CustomerLoginCode(customer_login_ui, self)

        self.setCentralWidget(customer_login_wid)

    def manager_login_func(self):
        self.bar_menu.setVisible(False)

        manager_login_wid = QtWidgets.QWidget()
        from frontend import ManagerLoginWid
        manager_login_ui = ManagerLoginWid()
        manager_login_ui.setupUi(manager_login_wid)
        from backend import ManagerLoginCode
        ManagerLoginCode(manager_login_ui, self)

        self.setCentralWidget(manager_login_wid)

    def chef_login_func(self):
        self.bar_menu.setVisible(False)

        chef_login_wid = QtWidgets.QWidget()
        from frontend import ChefLoginWid
        chef_login_ui = ChefLoginWid()
        chef_login_ui.setupUi(chef_login_wid)
        from backend import ChefLoginCode
        ChefLoginCode(chef_login_ui, self)

        self.setCentralWidget(chef_login_wid)

    def connect_func(self):
        self.bar_menu.setVisible(False)

        conn_wid = QtWidgets.QWidget()
        from frontend import ConnectWid
        conn_ui = ConnectWid()
        conn_ui.setupUi(conn_wid)
        from backend import ConnectCode
        ConnectCode(conn_ui, self)

        self.setCentralWidget(conn_wid)

    def manager_func(self):
        self.bar_menu.setVisible(True)

        manager_wid = QtWidgets.QWidget()
        from frontend import ManagerWid
        manager_ui = ManagerWid()
        manager_ui.setupUi(manager_wid)
        from backend import ManagerCode
        ManagerCode(manager_ui, self)

        self.setCentralWidget(manager_wid)

    def chef_func(self):
        self.bar_menu.setVisible(True)

        chef_wid = QtWidgets.QWidget()
        from frontend import ChefWid
        chef_ui = ChefWid()
        chef_ui.setupUi(chef_wid)
        from backend import ChefCode
        ChefCode(chef_ui, self)

        self.setCentralWidget(chef_wid)

    def customer_func(self):
        self.bar_menu.setVisible(True)

        customer_wid = QtWidgets.QWidget()
        from frontend import CustomerWid
        customer_ui = CustomerWid()
        customer_ui.setupUi(customer_wid)
        from backend import CustomerCode
        CustomerCode(customer_ui, self)

        self.setCentralWidget(customer_wid)

    def start_here(self):
        self.connect_func()


if __name__ == '__main__':
    AW = QtWidgets.QApplication(sys.argv)

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
