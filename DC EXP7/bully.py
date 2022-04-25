coordinator = 0
n = int(input(("Enter the number of process: ")))
status = []
priority = []


def Bulley(initiator):
    global coordinator
    initiator = initiator - 1
    coordinator = initiator + 1
    for i in range(n):
        if priority[initiator] < priority[i]:
            print(f"Election message is sent from {initiator+1} to {i+1}")
        if status[i] == 1:
            Bulley(i + 1)


for i in range(n):
    print(f"For Process {i+1}:")
    status.append(int(input("Status: ")))
    priority.append(i+1)
initiator = int(input("Which process will initiate election? "))
Bulley(initiator)
print(f"Final coordinator: {coordinator}")
