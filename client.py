import socket
import threading

nickname = input("Choose a nickname: ")  

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 62895))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error!')
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

recvThread = threading.Thread(target=receive)
recvThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()