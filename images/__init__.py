from PyQt5.QtGui import QIcon, QPixmap, QGuiApplication
import sys
temp = QGuiApplication(sys.argv)
im_correct = QPixmap("images\\correct.ico").scaled(30, 30)
im_enter = QPixmap("images\\enter.ico").scaled(30, 30)
ic_insert_table = QIcon("images\\insert_table.ico")
im_wrong = QPixmap("images\\wrong.ico").scaled(30, 30)
im_loading = QPixmap('images\\hourglass.ico').scaled(30, 30)
im_net_error = QPixmap('images\\exclamation5.ico').scaled(30, 30)
