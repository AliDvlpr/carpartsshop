import socket
s = socket.socket()
port = 12345
ip = 'localhost'
s.connect((ip,port))
print("connected")
print("hi welcome to car part shop select an operation:\n1 - see all available parts\n2 - find parts by name\n3 - find parts by id\n4 - buy parts with id\n")
while True:
    message = input("=>  ")
    s.send(message.encode())
    print(s.recv(1024).decode())