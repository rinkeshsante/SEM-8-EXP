from threading import Thread
from socket import socket


# lamport


class Process:

    def __init__(self, process, address) -> None:
        super.__init__()
        self.process_address = process_address
        self.address = address

    def request(self):
        for i in self.process_address:
            if i != self.address:
                pass

    def reply(self):
        pass

    def release(self):
        pass

    def run(self) -> None:
        while True:
            pass


process_address = [8000, 8001, 8002, 8003, 8004]
