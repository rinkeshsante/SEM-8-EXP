import time
from threading import RLock, Thread


class Shared:
    def __init__(self) -> None:
        self.lock = RLock()

    def test1(self, arg):
        with self.lock:
            print("test 1 begin")
            time.sleep(1)
            arg.test2(self)
            print("test 1 end")

    def test2(self, arg):
        with self.lock:
            print("test 2 begin")
            time.sleep(1)
            arg.test1(self)
            print("test 2 end")


class Thread1(Thread):
    def __init__(self, s1, s2):
        super().__init__()
        self.s1 = s1
        self.s2 = s2

    def run(self):
        self.s1.test1(self.s2)


class Thread2(Thread):
    def __init__(self, s1, s2):
        super().__init__()
        self.s1 = s1
        self.s2 = s2

    def run(self):
        self.s2.test2(self.s1)


s1 = Shared()
s2 = Shared()

t1 = Thread1(s1, s2)
t1.start()

t2 = Thread2(s1, s2)
t2.start()

time.sleep(2)
