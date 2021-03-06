from time import sleep
from mpi4py import MPI
import random
from heapq import *
import sys

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
REQUESTING_PROBABILITY = 0.01
if len(sys.argv) >= 2:
    REQUESTING_PROBABILITY = float(sys.argv[1])
local_time = 0


def update_local_time(new_timestamp):
    global local_time
    local_time = max(local_time + 1, new_timestamp + 1)


class RicartAgarwala:
    def __init__(self):
        self.defer_queue = {}
        self.REQUESTED = False
        self.nodes_replied = set()
        self.request_timestamp = (-1, -1, -1)

    def loop_node(self):
        req = comm.irecv()
        while True:
            if not self.REQUESTED and random.random() < REQUESTING_PROBABILITY:
                self.request()
            data = req.test()
            if data[0] == True:
                req = comm.irecv()
            if self.REQUESTED == True:
                if data[0] == True and data[1] is not None and data[1][2] == 0:
                    msg_timestamp = data[1][0]
                    sender = data[1][1]
                    update_local_time(msg_timestamp)
                    self.nodes_replied.add(sender)
                    if len(self.nodes_replied) == size - 1:
                        self.exec_cs()
                        self.REQUESTED = False
                        self.nodes_replied = set()
                        for i in self.defer_queue:
                            self.reply(i)
                        self.defer_queue = {}
                        self.request_timestamp = (-1, -1, -1)
            if data[0] == True and data[1] is not None and data[1][2] == 1:
                msg_timestamp = data[1][0]
                sender = data[1][1]
                update_local_time(msg_timestamp)
                if self.REQUESTED == False or self.request_timestamp[0] > msg_timestamp:
                    self.reply(sender)
                elif self.request_timestamp[0] == msg_timestamp and rank > sender:
                    self.reply(sender)
                else:
                    self.defer_queue[sender] = 1
                    print("DEFERRED:", self.defer_queue)

    def request(self):
        update_local_time(local_time)
        msg = (local_time, rank, 1)
        self.REQUESTED = True
        self.request_timestamp = msg
        for r in range(size):
            if r != rank:
                sleep(random.random())
                comm.send(msg, dest=r)

    def reply(self, receiver):
        if receiver != rank:
            update_local_time(local_time)
            msg = (local_time, rank, 0)
            sleep(random.random())
            comm.send(msg, dest=receiver)

    def exec_cs(self):
        print("executing cs for", rank, "... having timestamp ",
              self.request_timestamp, flush=True)
        update_local_time(local_time)
        critical_function()


def critical_function(filename1="tmp.txt"):
    with open(filename1, "w+") as f:
        f.write(str(rank))
    sleep(2)
    with open(filename1, "r") as f:
        line = f.readline().strip()
        if line == "" or int(line) != rank:
            print("\n\n\n******CS FAILED*****\nExpected {} found {}\n\n".format(rank,
                  int(line)), flush=True)
        else:
            print("CS PASSED", flush=True)


if __name__ == "__main__":
    algo = RicartAgarwala()
    algo.loop_node()
