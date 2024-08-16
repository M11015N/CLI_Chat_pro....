import socket
import os

def send_message(sock, target_address):
    message = input("plz write your message here end(or type 'file' to send a file): ")
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
target_ip = "127.0.0.1"  # single present
port_no = 2525
target_address = (target_ip, port_no)

while True:
    send_message(s, target_address)
    receive_message(s)
