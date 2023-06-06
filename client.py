import socket
s = socket.socket()
port = 12345
ip = 'localhost'
s.connect((ip,port))
print("connected")
while True:
    print(s.recv(1024).decode())
    message = input("=>  ")
    s.send(message.encode())