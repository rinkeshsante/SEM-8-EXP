from time import sleep
from mpi4py import MPI
import random
from heapq import *
from collections import deque

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

local_time = 0


def update_local_time(new_timestamp):
    global local_time
    local_time = max(local_time + 1, new_timestamp + 1)


class SuzukiKasami:
    def __init__(self):
        self.rn = [0 for i in range(size)]
        self.token = None
        self.REQUESTED = False
        if rank == 0:
            self.token = ([0 for i in range(size)], deque())

    def loop_node(self):
        req = comm.irecv()
        while True:
            if not self.REQUESTED and random.random() < 0.2:
                self.REQUESTED = True
                self.request()
            data = req.test()
            if data[0] == True:
                req = comm.irecv()
            if self.REQUESTED and self.token is not None:
                self.REQUESTED = False
                self.exec_cs()
                self.token[0][rank] = self.rn[rank]
                for j in range(size):
                    if self.rn[j] == self.token[0][j] + 1:
                        if j not in self.token[1]:
                            self.token[1].append(j)
                if len(self.token[1]) != 0:
                    top = self.token[1].popleft()
                    self.transfer_token(top)
            if data[0] == True and data[1] is not None and data[1][2] == 0:
                token = data[1][1]
                self.token = token
                print(token)
            if data[0] == True and data[1] is not None and data[1][2] == 1:
                sender = data[1][0]
                seq_no = data[1][1]
                self.rn[sender] = max(self.rn[sender], seq_no)
                if self.token is not None and self.rn[sender] == self.token[0][sender] + 1:
                    self.transfer_token(sender)

    def request(self):
        self.rn[rank] += 1
        msg = (rank, self.rn[rank], 1)
        for i in range(size):
            if i != rank:
                comm.send(msg, dest=i)

    def transfer_token(self, to):
        print("sending token from", rank, " to", to, flush=True)
        msg = (rank, self.token, 0)
        comm.send(msg, dest=to)
        self.token = None

    def exec_cs(self):
        print("executing cs for", rank, flush=True)
        update_local_time(local_time)
        critical_function()


def critical_function(filename1="tmp.txt"):
    with open(filename1, "w+") as f:
        f.write(str(rank))
    sleep(2)
    with open(filename1, "r") as f:
        line = f.readline().strip()
        if line == "" or int(line) != rank:
            print("\n\n\n******CS FAILED*****\n\n\n", flush=True)
        else:
            print("CS PASSED", flush=True)


algo = SuzukiKasami()
algo.loop_node()
