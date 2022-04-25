import socket
from _thread import start_new_thread
PORT = 6000


class MyServer:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("localhost", PORT))
        self.server.listen(100)

        self.list_of_client = []

    def startListening(self):
        while True:
            conn, addr = self.server.accept()

            self.list_of_client.append(conn)

            print(f"{addr} connected ..")

            start_new_thread(self.listen, (conn, addr))

    def listen(self, conn, address):
        conn.send("welcome to chat... ".encode())
        while True:
            try:
                msg = conn.recv(2048)
                if msg:
                    msg_to_send = f"<{address[0]}> {msg}".encode()
                    print(msg_to_send)
                    self.broadcast(conn, msg_to_send)
                else:
                    self.removeConn(conn)
            except:
                continue

    def broadcast(self, conn, msg):
        for client in self.list_of_client:
            if client != conn:
                try:
                    client.send(msg)
                except:
                    client.close()
                    self.removeClient(client)

    def removeClient(self, conn):
        if conn in self.list_of_client:
            self.list_of_client.remove(conn)


def main():
    server = MyServer()
    server.startListening()


if __name__ == '__main__':
    main()
