from PyQt5.QtCore import QThread, pyqtSignal


class ThreadUploadImage(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class

    def set_arg(self, food_id, location):
        self.food_id = food_id
        self.location = location

    def run(self):
        from pymongo.errors import AutoReconnect
        myc = self.parent_class.MW.DB.food
        try:
            if self.location:
                open_file = open(self.location, 'rb')
                im_data = open_file.read()
                open_file.close()

                ret_id = myc.update_one({'_id': self.food_id}, {'$set': {'food_image': im_data}})
                self.parent_class.MW.mess('Image Upload Successful')
            else:
                self.parent_class.MW.mess('Image Selection Rejected')
        except AutoReconnect:
            self.parent_class.MW.mess('-->> Network Error <<--')
