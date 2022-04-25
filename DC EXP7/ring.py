node = []
status = []
election = []

n = int(input("Enter no. of process: "))
for i in range(n):
    node.append(i + 1)
    status.append(int(input(f"Enter Status of process {i+1}: ")))

for i in range(len(node)):
    if status[i] != 0:
        election.append(node[i])

print(f"Coordinator is {max(election)}")
