import socket

class Cliente:
    PORT = 65432
    SERVER = "127.0.0.1"
    ADDR = (SERVER, PORT)
    FORMAT = "utf-8"

    @classmethod
    def connection(cls, data):
        client_socket = socket.socket(socket.AF_INET,
                                      socket.SOCK_STREAM)
        client_socket.connect(cls.ADDR)

        msg = data.encode(cls.FORMAT)

        client_socket.send(msg)
        client_socket.close()

if __name__ == "__main__":
    pass
