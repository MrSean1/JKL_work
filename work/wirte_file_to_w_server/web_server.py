# import socket
#
# HOST, PORT = '', 8888
#
# listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listen_socket.bind((HOST, PORT))
# listen_socket.listen(1)
# print('Serving HTTP on port %s ...' % PORT)
# while True:
#     client_connection, client_address = listen_socket.accept()
#     request = client_connection.recv(1024)
#     print(request)
#     print(request.title())
#
#     http_response = b"""
#     HTTP/1.1 200 OK
#     Hello, World!
#     """
#
#     client_connection.sendall(http_response)
#     client_connection.close()

import socket


def handle_request(client):
    buf = client.recv(1024)
    client.send(b"HTTP/1.1 200 OK\r\n\r\n")
    client.send(b"Hello, Seven")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8000))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()


if __name__ == '__main__':
    main()
