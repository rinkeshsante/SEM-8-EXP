from concurrent.futures import process
import queue

# suzuki kasami


class Token:
    def __init__(self) -> None:
        self.LN = queue.Queue()


class Process:
    def __init__(self, process_list) -> None:
        self.RN = process_list

    def passToken(self):
        pass
