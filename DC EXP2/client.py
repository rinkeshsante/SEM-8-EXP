import socket
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
data = input("Message:")
client.sendall(bytes(data, 'UTF-8'))

while True:
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())
    out_data = input("Message: ")
    client.sendall(bytes(out_data, 'UTF-8'))

    if out_data == 'bye':
        break

client.close()
