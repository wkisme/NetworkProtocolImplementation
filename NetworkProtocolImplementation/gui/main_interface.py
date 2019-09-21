import sys
import _thread
import time
from PyQt5.QtWidgets import QWidget, QLineEdit,\
    QPushButton, QApplication, QComboBox, QLabel
from tcp_communication.server import tcp_server
from tcp_communication.client import tcp_client
from udp_communication.client import udp_client
from udp_communication.server import udp_server
from chatroom.udp_chatroom import RunClient
from chatroom.udp_chatroom import RunServer
from ftp_program.ftp_client import ftp_client
from mail_transfer.mail_transfer import mail_transfer
from web_browser.webkit_browser import browser



class main_interface(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'main interface'
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 400
        self.main_interface()

    def main_interface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        tcp_button = QPushButton('tcp communication', self)
        tcp_button.clicked.connect(self.tcp_communication)
        tcp_button.move(0, 30)
        self.client_data = QLineEdit(self)
        self.client_data.setPlaceholderText('how are you sever ?')
        self.client_data.move(0, 0)
        self.tcp_result = QLineEdit(self)
        self.tcp_result.move(0, 60)
        self.tcp_result.resize(400, 20)

        udp_button = QPushButton('udp communication', self)
        udp_button.clicked.connect(self.udp_communication)
        udp_button.move(0, 120)
        self.udp_client_data = QLineEdit(self)
        self.udp_client_data.setPlaceholderText('how are you upd sever ?')
        self.udp_client_data.move(0, 90)
        self.udp_client_data.resize(200, 20)

        self.udp_result = QLineEdit(self)
        self.udp_result.move(0, 150)
        self.udp_result.resize(400, 20)

        self.chatroom_client_data = QLineEdit(self)
        self.chatroom_client_data.setPlaceholderText('how are you other clients ?')
        self.chatroom_client_data.move(0, 180)
        self.chatroom_client_data.resize(200, 20)
        self.chat_client_button = QPushButton('run clinet', self)
        self.chat_server_button = QPushButton('run server', self)
        self.chat_client_button.move(100, 210)
        self.chat_server_button.move(0, 210)
        self.chat_client_button.clicked.connect(self.chatroom_client)
        self.chat_server_button.clicked.connect(self.chatroom_server)
        self.chatroom_result = QLineEdit(self)
        self.chatroom_result.move(0, 230)
        self.chatroom_result.resize(400, 40)

        self.ftp_client_result = QLineEdit(self)
        self.ftp_client_result.move(0, 290)
        self.ftp_client_result.resize(400, 20)
        udp_button = QPushButton('ftp client', self)
        udp_button.clicked.connect(self.ftp_client)
        udp_button.move(0, 270)

        udp_button = QPushButton('mail transfer', self)
        udp_button.clicked.connect(self.mail_transfer)
        udp_button.move(0, 310)

        self.browser_input = QLineEdit(self)
        self.browser_input.move(0, 330)
        self.browser_input.resize(400, 20)
        browser_button = QPushButton('browser', self)
        browser_button.clicked.connect(self.browser)
        browser_button.move(0, 350)



        self.show()

    def browser(self):
        self.second_interface = browser(self.browser_input.text())
        self.second_interface.show()

    def mail_transfer(self):
        mail_transfer()

    def ftp_client(self):
        a = ftp_client()
        self.ftp_client_result.setText(a)

    def tcp_communication(self):

        _thread.start_new_thread(tcp_server, ())
        time.sleep(5)

        sent, receive = tcp_client(self.client_data.text())
        print(sent, receive)
        self.tcp_result.setText(sent + receive)

    def udp_communication(self):
        _thread.start_new_thread(udp_server, ())
        time.sleep(5)

        receive = udp_client(self.udp_client_data.text())
        print(receive)
        self.udp_result.setText(receive)

    def chatroom_client(self):
        receive = RunClient(self.chatroom_client_data.text())
        before_receive = self.chatroom_result.text()
        self.chatroom_result.setText(before_receive + '\n' + receive)

    def chatroom_server(self):
        _thread.start_new_thread(RunServer, ())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_interface()
    sys.exit(app.exec_())
