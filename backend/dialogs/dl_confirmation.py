from PyQt5.QtWidgets import QMessageBox


class DialogConfirmation(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle('Confirm')
        self.setInformativeText(message)
        self.setIcon(QMessageBox.Question)
        from images import ic_milkshake
        self.setWindowIcon(ic_milkshake)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
