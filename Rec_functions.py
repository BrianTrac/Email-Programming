import base64
import pytz
import uuid
import os
import time
from socket import *
from datetime import datetime, timedelta
from urllib.parse import unquote
from Rec_Email_Infor_Class import *


def connect_and_greet(client_socket, server, port):
    client_socket.connect((server, port))
    print(client_socket.recv(1024).decode('utf-8'))


def send_commands(client_socket, username, password):
    commands = [
        'CAPA',
        f'USER {username}',
        f'PASS {password}',
        'STAT',
        'LIST'
    ]

    # Send commands
    for command in commands:
        client_socket.send(f'{command}\r\n'.encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))


def get_email_index_list(client_socket):
    client_socket.send(b'LIST\r\n')
    response = b''
    while True:
        partial_response = client_socket.recv(1024)
        if not partial_response:
            break
        response += partial_response
        if b'\r\n.\r\n' in partial_response:
            break

    print(response.decode('utf-8'))

    # get index in list
    index_list = [line.split(b' ')[0].decode('utf-8')
                  for line in response.split(b'\r\n')]
    # # eliminate char that is not num
    index_list = [int(num) for num in index_list if num.isdigit()]

    return index_list


def get_retr_list(index_list, RETR_FILE):
    with open(RETR_FILE, 'a+') as retr_file:
        retr_file.seek(0)
        retr_data = retr_file.read()
        if (len(retr_data) == 0):
            retr_list = index_list
        else:
            retr_data = retr_data.split('\n')
            retr_data = retr_data[:len(retr_data) - 1]
            retr_list = [
                element for element in index_list if element not in map(int, retr_data)]
        retr_file.writelines([f'{element}\n' for element in retr_list])

    return retr_list


def get_and_save_raw_email(client_socket, element, PATH):
    # Create temporary text file to store raw email before parsing it
    temp_file_path = os.path.join(PATH, "temp_content.txt")
    open(temp_file_path, 'a').close()

    with open(temp_file_path, 'ab') as file:
        client_socket.send(f'RETR {element}\r\n'.encode('utf-8'))
        while True:
            partial_response = client_socket.recv(1024)
            if not partial_response:
                break
            file.write(partial_response)
            if b'\r\n.\r\n' in partial_response:
                break

    with open(temp_file_path, 'rb') as file:
        parse_mime_structure(file.read().decode('utf-8'), element, PATH)
    os.remove(temp_file_path)


def parse_mime_structure(message, element, PATH):
    # Split the message into headers and body
    headers, body = message.split('\r\n\r\n', 1)

    # Parse headers into a dictionary
    headers_dict = dict((line.split(": ", 1))
                        for line in headers.split('\r\n') if ": " in line)

    # Get the content type
    content_type = headers_dict.get('Content-Type', '')

    # Create a new folder name
    folder_name = f"{element}"

    # Specify the folder path
    folder_path = os.path.join(PATH, folder_name)

    # Create the new folder
    os.makedirs(folder_path)

    # get email info
    email_info = get_email_info(headers_dict)
    json_filename = f'{element}.json'
    json_file = os.path.join(folder_path, json_filename)
    email_info.save_to_json(email_info, json_file)

    # Check if it's a multipart message
    if 'multipart/mixed' in content_type:
        boundary = content_type.split('boundary=')[1].strip('"')
        parts = body.split(f'--{boundary}')
        parts = parts[1:(len(parts) - 1)]

        for part in parts:
            # Process each part
            if part and part != '--\r\n':
                process_mime_structure(folder_path, part)
    elif 'text/plain' in content_type:
        filename = 'content.txt'
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as file:
            file.write(body)
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            file.writelines(lines[:-5])
    else:
        pass


def get_email_info(headers_dict):
    email_info = EmailInfo()
    try:
        email_info.Date = headers_dict.get('Date', '')
    except:
        email_info.Date = ""

    try:
        email_info.To = headers_dict.get('To', '') | ""
    except:
        email_info.To = ""

    try:
        email_info.Cc = headers_dict.get('Cc', '')
    except:
        email_info.Cc = ""

    try:
        email_info.Subject = headers_dict.get('Subject', '')
    except:
        email_info.Subject = ""

    try:
        email_info.From = headers_dict.get('From', '')
    except:
        email_info.From = ""

    try:
        email_info.Content_Transfer_Encoding = headers_dict.get(
            'Content_Transfer_Encoding', '')
    except:
        email_info.Content_Transfer_Encoding = ""

    return email_info


def process_mime_structure(folder_path, part):
    # Extract headers and body for each part
    part_headers, part_body = part.split('\r\n\r\n', 1)

    # Parse headers into dictionary
    part_headers_dict = dict(
        (line.split(": ", 1) if ": " in line else line.split("=", 1))
        for line in part_headers.split('\r\n') if (": " in line or "filename" in line)
    )

    print(part_headers_dict)

    # Check if the part in an attachment
    if 'attachment' in part_headers_dict.get('Content-Disposition', ''):
        # Extract filename and content
        print(part_headers_dict.get('Content-Disposition', ''))
        if '=' in part_headers_dict.get('Content-Disposition', ''):
            filename = part_headers_dict.get(
                'Content-Disposition', '').split('=')[1].strip('"')
        else:
            filename = ""
    else:
        filename = 'content.txt'

    if filename == "":

        if ' filename' in part_headers_dict:
            filename = part_headers_dict.get(' filename', '').strip('"')
        elif ' filename*' in part_headers_dict:
            filename = part_headers_dict.get(
                ' filename*', '').split("UTF-8''")[1]
            filename = unquote(filename)
        elif ' filename*0' in part_headers_dict:
            filename = part_headers_dict.get(' filename*0', '').strip(";").strip(
                '"') + part_headers_dict.get(' filename*1', '').strip('"')
        elif ' filename*0*' in part_headers_dict:
            filename0 = part_headers_dict.get(
                ' filename*0*', '').split("UTF-8''")[1]
            filename0 = unquote(filename0).strip(';')
            filename1 = part_headers_dict.get(' filename*1*', '')
            filename1 = unquote(filename1).strip("' ")
            filename = filename0 + filename1
        else:
            filename = "Error.txt"

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


def quit_email(client_socket):
    client_socket.send(b'QUIT\r\n')
    print(client_socket.recv(1024).decode('utf-8'))


def receive_email(username, password):
    pop3_server = '127.0.0.1'
    pop3_port = 3335

    current_folder = os.path.dirname(os.path.abspath(__file__))
    user_folder = os.path.join(current_folder, username)
    if not os.path.exists(user_folder):
        os.mkdir(user_folder)
        Inbox_folder = os.path.join(user_folder, 'Inbox')
        os.mkdir(Inbox_folder)
        RETR_FILE = os.path.join(Inbox_folder, 'retrived.txt')
        open(RETR_FILE, 'a').close()
    else:
        Inbox_folder = os.path.join(user_folder, 'Inbox')
        RETR_FILE = os.path.join(Inbox_folder, 'retrived.txt')

    with socket(AF_INET, SOCK_STREAM) as client_socket:
        connect_and_greet(client_socket, pop3_server, pop3_port)
        send_commands(client_socket, username, password)

        index_list = get_email_index_list(client_socket)
        retr_list = get_retr_list(index_list, RETR_FILE)
        print(index_list)
        print(retr_list)

        for element in retr_list:
            get_and_save_raw_email(client_socket, element, Inbox_folder)
        quit_email(client_socket)


def is_server_running(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            return True
        except socket.error:
            return False


# Receive email
username = 'anhkhoa@gmail.com'
password = '12345678'
# receive_email(username, password)


def auto_receive_email(username, password, interval):
    while (True):
        try:
            pop3_server = '127.0.0.1'
            pop3_port = 3335
            with socket(AF_INET, SOCK_STREAM) as client_socket:
                connect_and_greet(client_socket, pop3_server, pop3_port)
        except Exception as e:
            print("Error: Could not connect to server.")
        else:
            receive_email(username, password)
            time.sleep(interval)



