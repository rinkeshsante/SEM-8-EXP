import mpi4py.MPI

comm = mpi4py.MPI.COMM_WORLD

rank = comm.Get_rank()


comm = mpi4py.MPI.COMM_WORLD

rank = comm.Get_rank()
counter = 0

for _ in range(3):
    if rank == 1:
        data = []
        counter += 1
        msg = f"Message : {counter}"
        comm.send(msg, dest=0)
    if rank == 0:
        msg = comm.recv(source=1)
        print(f"Recived : {msg}")
