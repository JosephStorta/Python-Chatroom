import threading
import socket

address = ""

while not address.replace(".", "").isdigit() or len(address.split(".")) != 4:
    address = input("Enter the IP address of the server: ")

    if not address.replace(".", "").isdigit() or len(address.split(".")) != 4:
        print("Please enter a valid IP address")

port = ""

while not port.isdigit():
    port = input("Enter the port of the server: ")

    if not port.isdigit():
        print("Please enter a valid port")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, int(port)))

nickname = input("Enter a nickname: ")

def receive():
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
    while True:
        message = f"{nickname}: {input("")}"
        client.send(message.encode("ascii"))

recieve_thread = threading.Thread(target = receive)
recieve_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()