import socket

host_ip, server_port = "127.0.0.1", 9999


def tcp_client(data):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9999))
    if result == 0:
        print("Port is open")

    else:
        print("Port is not open")

    sock.close()
    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print(host_ip, server_port)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(data.encode())

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()

    sent = "Bytes Sent:     " + data + '\n'
    receive = "Bytes Received: " + received.decode()

    print(sent, receive)
    return sent, receive

if __name__ == '__main__':
    tcp_client('i am client')
