import socket
import os

def send_message(sock, target_address):
    message = input("plz write your message here (or type 'file' to send a file): ")
    if message == 'file':
        file_path = input("Enter the path of the file to send: ")
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
                sock.sendto(b'file:' + file_path.encode('ascii') + b':' + file_data, target_address)
                print("File sent successfully.")
        else:
            print("File not found.")
    else:
        encrypted_message = message.encode('ascii')
        sock.sendto(encrypted_message, target_address)

def receive_message(sock):
    data, addr = sock.recvfrom(65535)
    if data.startswith(b'file:'):
        _, file_name, file_data = data.split(b':', 2)
        with open(file_name.decode('ascii'), 'wb') as file:
            file.write(file_data)
        print(f"Received file from {addr[0]}: {file_name.decode('ascii')}")
    else:
        print(f"Received message from {addr[0]}: {data.decode('ascii')}")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_address = "127.0.0.1"  # single person
port_no = 2525
complete_address = (ip_address, port_no)
s.bind(complete_address)

print("Hey, I am receiving your messages....")
while True:
    receive_message(s)
    send_message(s, complete_address)
