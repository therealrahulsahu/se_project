from PyQt5 import QtWidgets
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(640, 360)
        self.setWindowTitle('Cyber Restaurent')
        # self.setWindowIcon(ic_insert_table)
        self.logged_user = ''

        self.bar_menu = self.menuBar()
        self.menu_bar()

        self.bar_status = self.statusBar()
        self.status_bar()

        self.start()

    def menu_bar(self):

        quit_action = QtWidgets.QAction('&Quit Session', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Quit Session')
        # quit_action.triggered.connect(self.login_wid)

        file_menu = self.bar_menu.addMenu('&File')
        file_menu.addAction(quit_action)

    def status_bar(self):
        self.bar_status.showMessage('Ready to Go....')

    def start(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = MyWindow()
    win.show()

    end = app.exec_()
    if not end:
        try:
            win.myc.close()
        except AttributeError:
            pass

        sys.exit(end)
