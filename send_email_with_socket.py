import base64
import pytz
import uuid
import os
from socket import *
from datetime import datetime, timedelta
from urllib.parse import unquote

RETR_FILE = "D:\\Python\\Socket Programming\\Email\\retr_file.txt"
CONTENT_EMAIL_FILE = "content_email.txt"
PATH = "D:\\Python\\Socket Programming\\Email\\Inbox"

def parse_mime_structure(message, element):
    # Split the message into headers and body
    headers, body = message.split('\r\n\r\n', 1)

    # Parse headers into a dictionary
    headers_dict  = dict((line.split(": ", 1)) for line in headers.split('\r\n') if ": " in line)

    # Get the content type
    content_type = headers_dict.get('Content-Type', '')

    # Create a new folder name using the timestamp
    folder_name = f"{element}"

    # Specify the folder path
    folder_path = os.path.join(PATH, folder_name)

    # Create the new folder
    os.makedirs(folder_path)

    # Check if it's a multipart message
    if 'multipart/mixed'  in content_type:
        boundary = content_type.split('boundary=')[1].strip('"')
        parts = body.split(f'--{boundary}')
        parts = parts[1:(len(parts) - 1)]

        for part in parts:
            # Process each part
            if part and part != '--\r\n':
                process_mime_structure(folder_path ,part)
    elif 'text/plain' in content_type:
            filename = CONTENT_EMAIL_FILE
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'w') as file:
                file.write(body)
    else:
        pass

def process_mime_structure(folder_path, part):
    # Extract headers and body for each part
    part_headers, part_body = part.split('\r\n\r\n', 1)

    # Parse headers into dictionary
    part_headers_dict = dict(
        (line.split(": ", 1) if ": " in line else line.split("*=UTF-8''", 1))
        for line in part_headers.split('\r\n') if (": " in line or "*=UTF-8''" in line)
    )

    print( part_headers_dict )

    # Check if the part in an attachment
    if 'attachment' in part_headers_dict.get('Content-Disposition', ''):
        # Extract filename and content
        print(part_headers_dict.get('Content-Disposition', ''))
        if '=' in part_headers_dict.get('Content-Disposition', ''):
            filename = part_headers_dict.get('Content-Disposition', '').split('=')[1].strip('"')
        else:
            filename = ""  
    else:
        filename = CONTENT_EMAIL_FILE
    
    if filename == "":
        print(part_headers_dict.get(' filename', ''))
        filename = part_headers_dict.get(' filename', '')
        if (filename == ""):
            filename = part_headers_dict .get(' filename*0', '')
        filename = unquote(filename)
    
    content = part_body
    print(filename, "!!!")
    # Save to file
    save_attachment(folder_path, filename, content, part_headers_dict)

def save_attachment(folder_path, filename, content, part_headers_dict):
    # Combine the folder_path and filename
    file_path = os.path.join(folder_path, filename)

    if '7bit' in part_headers_dict.get('Content-Transfer-Encoding', '').strip():
        # Open the file and write content to it
        with open(file_path, 'wb') as file:
            file.write(content.encode('utf-8'))
        
    elif 'base64' in part_headers_dict.get('Content-Transfer-Encoding', '').strip():
        encoded_bytes = content.encode('utf-8')
        decoded_bytes = base64.b64decode(encoded_bytes)
        with open(file_path, 'wb') as file:
            file.write(decoded_bytes)
    else:
        pass

def get_email_index_list(client_socket):
    client_socket.send(b'LIST\r\n')
    response = receive_response(client_socket)
    print(response.decode('utf-8'))

    # get index in list
    index_list = [line.split(b' ')[0].decode('utf-8') for line in response.split(b'\r\n')] 
    # # eliminate char that is not num
    index_list = [int(num) for num in index_list if num.isdigit()]
    
    return index_list

def get_retr_list(index_list):
    with open(RETR_FILE, 'a+') as retr_file:
        retr_file.seek(0)
        retr_data = retr_file.read()
        if (len(retr_data) == 0):
            retr_list = index_list
        else:
            retr_data = retr_data.split('\n')
            retr_list = [element for element in index_list if element not in map(int, retr_data)]
        retr_file.writelines([f'\n{element}' for element in retr_list])

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
    #    'UIDL'
    ]

    responses = []

    # Send commands
    for command in commands:
        client_socket.send(f'{command}\r\n'.encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))

def receive_email(username, password):
    pop3_server = '127.0.0.1'
    pop3_port = 2000

    with socket(AF_INET, SOCK_STREAM) as client_socket:
        connect_and_greet(client_socket, pop3_server, pop3_port)
        send_commands(client_socket, username, password)

        index_list = get_email_index_list(client_socket)
        retr_list = get_retr_list(index_list)
        print (index_list)
        print (retr_list)

        for element in retr_list:
            response = retr_email(client_socket, element)
            parse_mime_structure(response.decode('utf-8'), element)

        quit_email(client_socket)

# Receive email
username = 'clientserver@gmail.com'
password = '12345678'
receive_email(username, password)
