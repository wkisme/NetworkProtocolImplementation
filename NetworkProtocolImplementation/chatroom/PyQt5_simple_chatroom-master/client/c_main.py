#!/usr/bin/env python3
# coding=utf-8

"""
图形用户界面, 主要有 5 个 class:

以下一个 class, 为套接字类
CliSoc(QUdpSocket)

以下四个 class 中, 每个 class 分别代表一个窗口控件
Popup(QMessageBox)
Login(QMainWindow)
Register(QMainWindow)
ChatRoom(QMainWindow)

"""

import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QPushButton,
    QLineEdit, QMainWindow, QLabel,
    QDesktopWidget,
)
from PyQt5.QtGui import QIcon

from conf.conf import QSS
from sub.qt_soc import CliSoc
from sub.qt_pop import Popup
from sub.qt_reg import Register
from sub.qt_chatroom import ChatRoom


# 登入界面
class Login(QMainWindow):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.initUI()
        self.box = Popup(self)
        self.chat_room = ChatRoom(self)
        self.reg_window = Register(self)
        self.soc = CliSoc(self)

    # 窗口居中方法
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        # 初始化设定
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(380, 220)
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())
        self.center()
        self.setStyleSheet(QSS)

        # 输入框前文字
        l_user = QLabel("用户名", self)
        l_user.move(60, 20)
        l_pswd = QLabel("密码", self)
        l_pswd.move(60, 60)
        l_addr = QLabel("服务器地址", self)
        l_addr.move(60, 100)

        # 输入框
        user = self.user_ = QLineEdit(self)
        user.move(120, 20)
        user.resize(200, 30)
        pswd = self.pswd_ = QLineEdit(self)
        pswd.setEchoMode(QLineEdit.Password)
        pswd.move(120, 60)
        pswd.resize(200, 30)
        addr = self.addr_ = QLineEdit(self)
        addr.move(140, 100)
        addr.resize(180, 30)

        # 按键
        btn_login = self.btn_login = QPushButton("Login", self)
        btn_login.move(70, 150)
        btn_register = QPushButton("Register", self)
        btn_register.move(210, 150)

        # 按键事件激发后, 调用方法
        btn_login.clicked.connect(self.buttonClicked)
        btn_register.clicked.connect(self.buttonClicked)

        # 显现
        self.show()

    # 按键事件被激发调用的方法, 主要作为外模块接口
    def buttonClicked(self, e):

        sender = self.sender()
        text = sender.text()
        self.soc.ip = self.addr_.text()
        # print(text)
        if text == "Login":
            user = self.user_.text()
            pswd = self.pswd_.text()
            # msg 将作为发送至服务器的内容
            msg = "%s|%s|%s" % (text, user, pswd)
            # print(msg)
            self.soc.send_msg(msg)
            self.recv_msg()
        elif text == "Register":
            self.reg_window.show()
            if self.reg_window.isVisible():
                self.hide()

    # recvmsg 负责接收服务器信息, 若为 False, 弹出密码错误信息, 将不得进入聊天室
    def recv_msg(self):
        time.sleep(0.1)
        recvmsg = self.soc.recv_msg()
        if recvmsg == '1':
            self.chat_room.user = self.user_.text()
            self.chat_room.show()
            self.soc.readyRead.connect(self.chat_room.recvMsg)
            if self.chat_room.isVisible():
                # self.hide()
                # 回报已在聊天室, 确认正常进入聊天室
                msg = "InRoom|%s|!" % self.chat_room.user
                self.soc.send_msg(msg)
        elif recvmsg == '0':
            self.box.setText('用户名或密码错误')
            self.box.show()
        elif recvmsg == '2':
            self.box.setText('该用户已在聊天室')
            self.box.show()
        else:
            print(recvmsg)


if __name__ == "__main__":

    # QApplication 必须插入
    app = QApplication(sys.argv)
    lgn = Login()
    sys.exit(app.exec_())
