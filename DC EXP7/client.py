import socket
from _thread import start_new_thread
Port = 6000


class Myclient:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(sys.argv[0])
        self.client.connect(("localhost", Port))

    def listen(self):
        while True:
            msg = self.client.recv(2048)
            print(msg)

    def connect(self):
        start_new_thread(self.listen, ())

    def send(self, msg: str):
        self.client.send(msg.encode())


def main():
    client = Myclient()
    client.connect()
    while True:
        msg = input()
        client.send(msg)


if __name__ == '__main__':
    main()
