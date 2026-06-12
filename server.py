import threading
import socket

host = "127.0.0.1" # Localhost
port = 62895

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 and uses TCP
server.bind((host, port))   
server.listen();

clients = []    # Store clients
nicknames = []  # Store server

def broadcast(message):     # Sends message to all clients
    for client in clients:
        client.send(message);

def handle(client):     
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():      
    while True:         # Loop forever, always waiting for new connections
        client, address = server.accept()       # Gets the client IP and Port
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))     # Asks for client nickname
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)  # Adds nickname to list
        clients.append(client)  # Adds client to list

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))   # Tells all clients that you joined
        client.send('Connected to the server!'.encode('ascii'))     

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()  # Creates and starts thread

print('Server is on')
receive()