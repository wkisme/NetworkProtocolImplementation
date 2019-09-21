import time
from PyQt5.QtWidgets import (
    QMainWindow, QDesktopWidget, QLabel, QLineEdit,
    QPushButton,
)
from PyQt5.QtGui import QCloseEvent

from .qt_pop import Popup


# 注册界面
class Register(QMainWindow):

    # 可以复制粘贴自 class Login, 需要多加密码条

    def __init__(self, parent=None):
        super(Register, self).__init__(parent)

        self.box = Popup(self)  # 此处是耦合的体现
        self.initUI()

    # 居中显示
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        # 初始化设定
        self.setWindowTitle("Register")
        self.resize(380, 220)
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())
        self.center()

        # 输入框前文字
        l_user = QLabel("用户名", self)
        l_user.move(50, 20)
        l_pswd0 = QLabel("密码", self)
        l_pswd0.move(50, 60)
        l_pswd1 = QLabel("确认密码", self)
        l_pswd1.move(50, 100)

        # 输入框
        user = self.user_ = QLineEdit(self)
        user.setPlaceholderText("用户长度至少3字符")
        user.move(120, 20)
        user.resize(200, 30)

        pswd0 = self.pswd_0 = QLineEdit(self)
        pswd0.setEchoMode(QLineEdit.Password)  # 使密码框密文显示
        pswd0.setPlaceholderText("密码长度至少6字符")
        pswd0.move(120, 60)
        pswd0.resize(200, 30)

        pswd1 = self.pswd_1 = QLineEdit(self)
        pswd1.setEchoMode(QLineEdit.Password)  # 使密码框密文显示
        pswd1.move(120, 100)
        pswd1.resize(200, 30)

        # 按键
        btn_register = QPushButton("Register", self)
        btn_register.move(70, 150)
        btn_back = QPushButton("Back", self)
        btn_back.move(210, 150)

        # 按键事件触发后, 调用方法
        btn_register.clicked.connect(self.buttonClicked)
        btn_back.clicked.connect(self.close)

        # 显现 if self.parent is None
        # self.show()

    def buttonClicked(self):

        sender = self.sender()
        text = sender.text()
        print(text)
        if text == "Register":
            user = self.user_.text()
            pswd0 = self.pswd_0.text()
            pswd1 = self.pswd_1.text()
            if pswd0 != pswd1:
                self.box.setText("两次输入密码不一致")
                self.box.show()
            elif len(user) < 3 or len(pswd0) < 6:
                self.box.setText("用户名或密码输入长度过短")
                self.box.show()
            else:
                msg = "%s|%s|%s" % (text, user, pswd0)
                # 下行应向服务器发送 msg
                print(msg)
                self.parent().soc.send_msg(msg)
                time.sleep(0.1)
                recvmsg = self.parent().soc.recv_msg()
                # 若 recvmsg 为 False, 将不得注册
                if recvmsg == '1':
                    self.box.setText("注册成功")
                    self.box.show()
                    self.close()
                elif recvmsg == '2':
                    self.box.setText("该用户已存在")
                    self.box.show()
                else:
                    print(recvmsg)

    # 当窗口关闭事件被触发
    def closeEvent(self, event):
        if self.parent and type(event) is QCloseEvent:
            # 下面应当发送退出消息
            self.parent().show()
