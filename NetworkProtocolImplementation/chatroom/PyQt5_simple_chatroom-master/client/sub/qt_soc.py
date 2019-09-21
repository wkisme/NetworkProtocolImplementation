
from PyQt5.QtNetwork import QUdpSocket, QHostAddress


# 套接字
class CliSoc(QUdpSocket):

    def __init__(self, parent=None, conn_ip='127.0.0.1'):
        super(CliSoc, self).__init__(parent)

        # 定义目标地址及端口号
        try:
            self.ip = conn_ip
            self.addr = QHostAddress(self.ip)
            self.conn_port = 30080
            self.connectToHost(self.addr, self.conn_port)
        except Exception as err:
            print(err)
            # 应该报告连接失败, 但暂时尝试连入 localhost
            self.ip = '127.0.0.1'
            self.addr = QHostAddress(self.ip)
            self.conn_port = 30080
            self.connectToHost(self.addr, self.conn_port)

    def send_msg(self, msg=None):
        # 向目标写入数据报
        self.writeDatagram(msg.encode(), self.addr, self.conn_port)
        self.flush()

    def recv_msg(self):
        # 获取数据报
        print("recv_msg被调用")
        buf, ip, port = self.readDatagram(1024)
        print(buf)
        print(ip.toString())
        print(port)
        try:
            if port == self.conn_port:
                msg = buf.decode()
            else:
                msg = 'Error|Other|FromOtherPort'
        except Exception as err:
            print(err)
            msg = 'Error|Self|Error'
        finally:
            self.flush()
            return msg
