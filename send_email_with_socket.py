import pytz
import uuid
import os
from socket import *
from datetime import datetime, timedelta

RETR_FILE = "D:\\Python\\Socket Programming\\Email\\retr_file.txt"
CONTENT_EMAIL_FILE = "content_email.txt"
PATH = "D:\\Python\\Socket Programming\\Email\\Inbox"

def receive_email(username, password):
    pop3_server = '127.0.0.1'
    pop3_port = 2000

    with socket(AF_INET, SOCK_STREAM) as client_socket:
        connect_and_greet(client_socket, pop3_server, pop3_port)
        send_commands(client_socket, username, password)
        index_list = get_email_index_list(client_socket)
        retr_list = get_retr_list(index_list)

        for element in retr_list:
            response = retr_email(client_socket, element)
            parse_mime_structure(response.decode('utf-8'), element)

        quit_email(client_socket)

def connect_and_greet(client_socket, server, port):
    client_socket.connect((server, port))
    print(client_socket.recv(1024).decode('utf-8'))

def send_commands(client_socket, username, password):
    commands = [
        'CAPA', 
        f'USER {username}', 
        f'PASS {password}', 
        'STAT', 
        'LIST', 
        'UIDL'
    ]

    for command in commands:
        client_socket.send(f'{command}\r\n'.encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))

def get_email_index_list(client_socket):
    client_socket.send(b'LIST\r\n')
    response = receive_response(client_socket)
    print(response.decode('utf-8'))

    index_list = [int(line.split()[0]) for line in response.split(b'\r\n') if line.strip().isdigit()]
    return index_list

def get_retr_list(index_list):
    with open(RETR_FILE, 'a+') as retr_file:
        retr_file.seek(0)
        retr_data = retr_file.read().split('\n')
        retr_list = [element for element in index_list if element not in map(int, retr_data)]
        retr_file.writelines([f'{element}\n' for element in retr_list])

    return retr_list

def retr_email(client_socket, element):
    client_socket.send(f'RETR {element}\r\n'.encode('utf-8'))
    response = receive_response(client_socket)
    print(response.decode('utf-8'))
    return response

def quit_email(client_socket):
    client_socket.send(b'QUIT\r\n')
    print(client_socket.recv(1024).decode('utf-8'))

def receive_response(client_socket):
    response = b''
    while True:
        partial_response = client_socket.recv(1024)
        if not partial_response:
            break
        response += partial_response
        if b'\r\n.\r\n' in partial_response:
            break
    return response

def parse_mime_structure(message, element):
    headers, body = message.split(b'\r\n\r\n', 1)
    headers_dict = dict(line.split(b": ", 1) for line in headers.split(b'\r\n') if b": " in line)
    content_type = headers_dict.get(b'Content-Type', b'')

    folder_name = f"{element}"
    folder_path = os.path.join(PATH, folder_name)
    os.makedirs(folder_path)

    if b'multipart/mixed' in content_type:
        boundary = content_type.split(b'boundary=')[1].strip(b'"')
        parts = body.split(f'--{boundary}'.encode('utf-8'))
        parts = parts[1:(len(parts) - 1)]

        for part in parts:
            if part and part != b'--\r\n':
                process_mime_structure(folder_path, part)
    elif b'text/plain' in content_type:
        filename = CONTENT_EMAIL_FILE
        save_attachment(folder_path, filename, body)
    else:
        pass

def process_mime_structure(folder_path, part):
    part_headers, part_body = part.split(b'\r\n\r\n', 1)
    part_headers_dict = dict(line.split(b": ", 1) for line in part_headers.split(b'\r\n') if b": " in line)

    if b'attachment' in part_headers_dict.get(b'Content-Disposition', b''):
        filename = part_headers_dict.get(b'Content-Disposition', b'').split(b'=')[1].strip(b'"')
        content = part_body.strip()
    else:
        filename = CONTENT_EMAIL_FILE
        content = part_body.strip()

    save_attachment(folder_path, filename, content)

def save_attachment(folder_path, filename, content):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as file:
        file.write(content)

# Receive email
username = 'clientserver@gmail.com'
password = '12345678'
receive_email(username, password)
