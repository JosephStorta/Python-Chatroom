import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []
nicknames = []

def broadcast(message):
    """Send a message to every client."""
    for client in clients:
        client.send(message)

def handle(client):
    """Receive messages from a client until the client closes."""
    while True:
        try:
            message = client.recv(1024) # Waits to receive a message from the client
            broadcast(message) # Broadcasts the message to every client
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat".encode("ascii"))
            nicknames.remove(nickname)
            break

def recieve():
    """Main server loop. Connects clients and transmits messages."""
    while True:
        client, address = server.accept() # Connects any clients that want to connect
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii")) # Send "NICK" to the new client to let it know we want its nickname
        nickname = client.recv(1024).decode("ascii") # Receive the client's nickname
        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))
        client.send("Connected to server".encode("ascii"))

        thread = threading.Thread(target = handle, args = (client,)) # Starts a new thread to handle the client
        thread.start()

if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname()) # Gets the IP of the host
    port = 55555

    server.bind((host, port))
    server.listen()

    print(f"Server active on address {host}:{port}")
    recieve()
