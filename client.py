import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nickname = ""

def receive():
    """Read messages sent from the server."""
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break

def write():
    """Send messages to the server."""
    while True:
        message = f"{nickname}: {input("")}"
        client.send(message.encode("ascii"))

def get_address() -> str:
    address = ""

    while not address.replace(".", "").isdigit() or len(address.split(".")) != 4:
        address = input("Enter the IP address of the server: ")

        if not address.replace(".", "").isdigit() or len(address.split(".")) != 4:
            print("Please enter a valid IP address")

    return address

def get_port() -> str:
    port = ""
    
    while not port.isdigit():
        port = input("Enter the port of the server: ")

        if not port.isdigit():
            print("Please enter a valid port")

    return port

if __name__ == "__main__":
    address = get_address()
    port = get_port()
    nickname = input("Enter a nickname: ")

    client.connect((address, int(port)))

    recieve_thread = threading.Thread(target = receive)
    recieve_thread.start()

    write_thread = threading.Thread(target = write)
    write_thread.start()