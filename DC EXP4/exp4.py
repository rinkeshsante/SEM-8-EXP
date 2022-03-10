import time
import random
import os

no_of_servers = int(input("Enter No of servsers : "))
threshold = int(input("Threshold for servers : "))
servers = [0] * no_of_servers


while True:
    server_no = random.randint(0, no_of_servers-1)
    if servers[server_no] >= threshold:
        if servers == [threshold] * no_of_servers:
            print("Stopping...")
            exit(0)
        continue
    os.system("cls")
    servers[server_no] += 1
    for i in range(no_of_servers):
        print(f"server{i}\t", end="")
    print()
    for i in range(no_of_servers):
        print(f"{servers[i]}\t", end="")
    print()
    time.sleep(.1)
