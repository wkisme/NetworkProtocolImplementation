from PyQt5.QtWidgets import QMessageBox


# 弹出信息, 传入 msg
class Popup(QMessageBox):

    def __init__(self, parent=None, msg=None):
        super(Popup, self).__init__(parent)

        self.initUI(msg)

    def initUI(self, msg):

        self.setWindowTitle("Infomation")
        self.setText(msg)
