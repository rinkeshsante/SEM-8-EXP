import socket
from threading import Thread


class ClientThread(Thread):
    def __init__(self, address):
        self.address = address
        print("[+] New server socket thread started at ", self.address)

    def run(self):
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind(self.address)

        while True:
            data = tcpServer.recv()
            print("Server received data:", data.decode())
            MESSAGE = input(
                "Multithreaded Python server: Enter Response from Server/Enter exit: ")
            if MESSAGE == 'exit':
                break
            tcpServer.send(MESSAGE.encode())  # echo


def main():
    # Multithreaded Python server : TCP Server Socket Program Stub
    TCP_IP = '0.0.0.0'
    TCP_PORT = 2004
    BUFFER_SIZE = 20  # Usually 1024, but we need quick response

    threads = []

    while True:
        tcpServer.listen(4)
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        (conn, (ip, port)) = tcpServer.accept()

        newthread = ClientThread(ip, port)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
