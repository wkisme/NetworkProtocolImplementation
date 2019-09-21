import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication


class browser(QWebEngineView):
    def __init__(self, input):
        super().__init__()
        self.title = input
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400
        self.second_window_interface()

    def second_window_interface(self):
        self.load(QUrl(self.title))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = browser('https://www.baidu.com')
    sys.exit(app.exec_())