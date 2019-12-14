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

        self.mess = self.statusBar().showMessage

        self.showMaximized()

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

        self.file_actions()
        self.show_actions()
        self.cache_actions()

    def file_actions(self):
        file_menu = self.bar_menu.addMenu('&File')

        from PyQt5.QtWidgets import QAction
        self.quit_action = QAction('&Quit Session', self)
        self.quit_action.setShortcut('Ctrl+Q')
        self.quit_action.setStatusTip('Quit Session')
        self.quit_action.triggered.connect(self.select_func)

        file_menu.addAction(self.quit_action)

    def show_actions(self):
        show_menu = self.bar_menu.addMenu('&Show')

        from PyQt5.QtWidgets import QAction
        maximise_action = QAction('&Maximise Window', self)
        maximise_action.setShortcut('Ctrl+M')
        maximise_action.setStatusTip('Maximise Window')
        maximise_action.triggered.connect(self.showMaximized)
        show_menu.addAction(maximise_action)

        fullscreen_action = QAction('&Full Screen', self)
        fullscreen_action.setShortcut('Ctrl+F')
        fullscreen_action.setStatusTip('Full Screen')
        fullscreen_action.triggered.connect(self.showFullScreen)
        show_menu.addAction(fullscreen_action)

        normal_screen_action = QAction('&Normal Window', self)
        normal_screen_action.setShortcut('Ctrl+N')
        normal_screen_action.setStatusTip('Normal Screen')
        normal_screen_action.triggered.connect(self.showNormal)
        show_menu.addAction(normal_screen_action)

        minimise_screen_action = QAction('&Minimise Window', self)
        minimise_screen_action.setShortcut('Ctrl+B')
        minimise_screen_action.setStatusTip('Minimise Window')
        minimise_screen_action.triggered.connect(self.showMinimized)
        show_menu.addAction(minimise_screen_action)

    def cache_actions(self):
        def action():
            from os.path import expanduser, join
            from shutil import rmtree
            try:
                rmtree(join(expanduser('~'), 'Documents', 'Cyber_Temp', 'Photos'))
                self.mess('Cache Cleared')
            except FileNotFoundError:
                self.mess('Cache Not Found')

        cache_menu = self.bar_menu.addMenu('&Cache')

        from PyQt5.QtWidgets import QAction
        self.clear_cache_action = QAction('&Clear Cache', self)
        self.clear_cache_action.setShortcut('Ctrl+Alt+C')
        self.clear_cache_action.setStatusTip('Clear Cache')
        self.clear_cache_action.triggered.connect(action)

        cache_menu.addAction(self.clear_cache_action)

    def select_func(self):
        self.quit_action.setEnabled(False)
        self.logged_user = ''

        from PyQt5.QtWidgets import QWidget
        select_wid = QWidget(self)
        from frontend import SelectWid
        select_ui = SelectWid()
        select_ui.setupUi(select_wid)
        from backend import SelectCode
        code = SelectCode(select_ui, self)

        self.setCentralWidget(select_wid)

    def customer_login_func(self):
        self.quit_action.setEnabled(False)

        from PyQt5.QtWidgets import QWidget
        customer_login_wid = QWidget(self)
        from frontend import CustomerLoginWid
        customer_login_ui = CustomerLoginWid()
        customer_login_ui.setupUi(customer_login_wid)
        from backend.customer import CustomerLoginCode
        code = CustomerLoginCode(customer_login_ui, self)

        self.setCentralWidget(customer_login_wid)

    def manager_login_func(self):
        self.quit_action.setEnabled(False)

        from PyQt5.QtWidgets import QWidget
        manager_login_wid = QWidget(self)
        from frontend import ManagerLoginWid
        manager_login_ui = ManagerLoginWid()
        manager_login_ui.setupUi(manager_login_wid)
        from backend.manager import ManagerLoginCode
        code = ManagerLoginCode(manager_login_ui, self)

        self.setCentralWidget(manager_login_wid)

    def chef_login_func(self):
        self.quit_action.setEnabled(False)

        from PyQt5.QtWidgets import QWidget
        chef_login_wid = QWidget(self)
        from frontend import ChefLoginWid
        chef_login_ui = ChefLoginWid()
        chef_login_ui.setupUi(chef_login_wid)
        from backend.chef import ChefLoginCode
        code = ChefLoginCode(chef_login_ui, self)

        self.setCentralWidget(chef_login_wid)

    def connect_func(self):
        self.quit_action.setEnabled(False)

        from PyQt5.QtWidgets import QWidget
        conn_wid = QWidget(self)
        from frontend import ConnectWid
        conn_ui = ConnectWid()
        conn_ui.setupUi(conn_wid)
        from backend import ConnectCode
        code = ConnectCode(conn_ui, self)

        self.setCentralWidget(conn_wid)

    def manager_func(self):
        self.quit_action.setEnabled(True)

        from PyQt5.QtWidgets import QWidget
        manager_wid = QWidget(self)
        from frontend import ManagerWid
        manager_ui = ManagerWid()
        manager_ui.setupUi(manager_wid)
        from backend import ManagerCode
        code = ManagerCode(manager_ui, self)

        self.setCentralWidget(manager_wid)

    def chef_func(self):
        self.quit_action.setEnabled(True)

        from PyQt5.QtWidgets import QWidget
        chef_wid = QWidget(self)
        from frontend import ChefWid
        chef_ui = ChefWid()
        chef_ui.setupUi(chef_wid)
        from backend import ChefCode
        code = ChefCode(chef_ui, self)

        self.setCentralWidget(chef_wid)

    def customer_func(self):
        self.quit_action.setEnabled(True)

        from PyQt5.QtWidgets import QWidget
        customer_wid = QWidget(self)
        from frontend import CustomerWid
        customer_ui = CustomerWid()
        customer_ui.setupUi(customer_wid)
        from backend import CustomerCode
        code = CustomerCode(customer_ui, self)

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
