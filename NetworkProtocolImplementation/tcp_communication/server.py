import socketserver
import socket

from psutil import process_iter
from signal import SIGKILL
import time
host, port = "localhost", 9999


class HandlerTCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.

    """

    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} sent:".format(self.client_address[0]))
        # print(self.data)
        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())


def tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9999))
    if result == 0:
        print("Port is open")

    else:
        flag = 0
        # for proc in process_iter():
        #     for conns in proc.connections(kind='inet'):
        #         if conns.laddr[1] == 9999:
        #             proc.send_signal(SIGKILL)
        #             break

        while True:

            try:

                print("Port is not open")
                # Init the TCP server object, bind it to the localhost on 9999 port
                tcp_server = socketserver.TCPServer((host, port), HandlerTCPServer)
                print("Port is open")
                # Activate the TCP server.
                # To abort the TCP server, press Ctrl-C.
                tcp_server.serve_forever()
                flag = 1

            except:
                time.sleep(5)
                continue

    sock.close()


if __name__ == '__main__':
    tcp_server()
