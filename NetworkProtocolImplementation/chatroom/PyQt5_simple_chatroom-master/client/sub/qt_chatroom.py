import time
from PyQt5.QtWidgets import (
    QMainWindow, QDesktopWidget, QPushButton,
    QTextBrowser, QTextEdit,
)
from PyQt5.QtGui import QTextCursor, QCloseEvent


# 聊天室界面
class ChatRoom(QMainWindow):

    msgLst = []

    def __init__(self, parent=None, user=None):
        super(ChatRoom, self).__init__(parent)

        self.user = user
        self.initUI()
        self.newMsg()

    # 居中显示
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        # 初始化
        self.setWindowTitle("Chatroom")
        self.resize(640, 480)
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())
        self.center()

        # 创建文本浏览区域
        textBrowser = self.textBrowser = QTextBrowser(self)
        textBrowser.resize(620, 240)
        textBrowser.move(10, 30)
        textBrowser.ensureCursorVisible()
        textBrowser.textChanged.connect(self.Scr)

        # 创建文本区域
        textEdit = self.textEdit = QTextEdit(self)
        textEdit.resize(620, 120)
        textEdit.move(10, 300)
        textEdit.ensureCursorVisible()

        # 创建发送按钮
        btnSend = QPushButton("Send", self)
        btnSend.move(270, 435)

        # 触发按钮事件后, 调用方法
        btnSend.clicked.connect(self.buttonClicked)

        # 显现 if self.parent is None
        # self.show()

    def buttonClicked(self):

        sender = self.sender()
        text = sender.text()
        if text == "Send":
            content = self.textEdit.toPlainText()
            print(content)
            if content:
                # 如果消息内容非空, 干活
                # self.content_ = (
                #     "%s|%s|%s" %
                #     (text, self.user, content)
                # )  # 临时变量, 传到 textBrowser
                msg = (
                    "%s|%s @ %s|%s" %
                    (text, self.user, time.ctime(), content)
                )
                self.parent().soc.send_msg(msg)
            # 清空文本编辑栏
            self.textEdit.setText('')

    def recvMsg(self):
        recvmsg = self.parent().soc.recv_msg()
        print(recvmsg)
        if recvmsg:
            msgLst = recvmsg.split('|')
            if msgLst[0] == 'Send':
                self.msgLst.append(recvmsg)
                # 当有新信息调用 newMsg
                self.newMsg()
            else:
                pass

    # 当消息行数大于框内显示行数, 自动滚动到末端
    def Scr(self):
        text_cursor = QTextCursor()
        self.textBrowser.moveCursor(text_cursor.End)

    # 如果传入的字符串的第一个单词为 'Send', 才能使用此方法
    def newMsg(self):

        msg = ''
        # 如果消息列表长度大于 500, 去除最早的消息
        if len(self.msgLst) > 500:
            del self.msgLst[0]
        print(self.msgLst)

        # 遍历消息列表, 刷新 textBrowser 内容
        for x in self.msgLst:
            lst = x.split("|")
            # cmd = lst[0]
            # 获取用户名称
            usr_time = lst[1]
            usr = usr_time.split(' @ ')[0]
            content = "|".join(lst[2:])
            print(content)
            contentLst = content.split("\n")
            align = "left"
            # 如果是本人发出的信息, 显示蓝色, 否则显示绿色
            if usr == self.user:
                msg += "<span style='color: #11d;'>%s</span><br>" % usr_time
            elif '管理员' in usr:
                msg += "<span style='color: purple;'>%s</span><br>" % usr_time
            else:
                msg += "<span style='color: #1d1;'>%s</span><br>" % usr_time
            for y in contentLst:
                msg += ('<span>%s</span><br>' % y)
            msg = "<div align='%s'>%s</div>" % (align, msg)
        self.textBrowser.setHtml("<body>%s</body>" % msg)

    # 当窗口关闭事件被触发
    def closeEvent(self, event):
        if self.parent and type(event) is QCloseEvent:
            # 下面应当发送退出消息
            self.parent().soc.send_msg('%s|%s|%s' % ('Quit', self.user, '1'))
            self.parent().show()
