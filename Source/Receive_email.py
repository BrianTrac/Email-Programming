import base64
import pytz
import uuid
import os
import time
from socket import *
from datetime import datetime, timedelta
from urllib.parse import unquote
import json
import shutil
from content_frame import ContentFrame

with open('filter.json', 'r') as file:
    FILTER = json.load(file)

with open('config.json', 'r') as file:
    CONFIG = json.load(file)

class EmailInfo:
    def __init__(self, Date=None, To=None, Cc=None, Bcc=None, From=None, Subject=None, Content_Transfer_Encoding=None):
        self.Date = Date
        self.From = From
        self.To = To
        self.Cc = Cc
        self.Bcc = Bcc
        self.From = From
        self.Subject = Subject
        self.Content_Transfer_Encoding = Content_Transfer_Encoding
        self.isClicked = str(False)
        self.isRead = str(False)
        self.isStar = str(False)
        try:
            self.Pre_Folder = os.path.join(CONFIG["Usermail"], str("Inbox"))
        except Exception as e:
            print(e)

    def to_dict(self):
        return {
            'Date': self.Date,
            'To': self.To,
            'Cc': self.Cc,
            'Bcc': self.Bcc,
            'From': self.From,
            'Subject': self.Subject,
            'Content_Transfer_Encoding': self.Content_Transfer_Encoding,
            'Clicked': self.isClicked,
            'Star': self.isStar,
            'Read': self.isRead,
            'Pre_Folder': self.Pre_Folder
        }

    def save_to_json(self, obj, filename):
        with open(filename, 'w') as file:
            json.dump(obj.to_dict(), file)

    def load_from_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return EmailInfo(data['Date'], data['To'], data['Cc'], data['Bcc'], data['From'], data['Subject'], data['Content_Transfer_Encoding'])

    def mark_as_read(self):
        self.isRead = True


class receive_email:
    def __init__(self, username, password, server, port):
        self.username = username
        self.password = password
        self.server = server
        self.port = port

        # Create an Inbox folder to store received emails
        self.current_folder_path = os.path.dirname(os.path.abspath(__file__))
        self.user_email_path = os.path.join(
            self.current_folder_path, self.username)
        if not os.path.exists(self.user_email_path):
            os.mkdir(self.user_email_path)

        for dir in FILTER.keys():
            if not os.path.exists(os.path.join(self.user_email_path, dir)):
                os.mkdir(os.path.join(self.user_email_path, dir))

        if not os.path.exists(os.path.join(self.user_email_path, "Inbox")):
            os.mkdir(os.path.join(self.user_email_path, "Inbox"))
        self.Inbox_path = os.path.join(self.user_email_path, "Inbox")
        
        self.msg_folder_path = os.path.join(self.user_email_path, 'msg')
        if not os.path.exists(self.msg_folder_path):
            os.mkdir(self.msg_folder_path)

        self.retrived_list_path = os.path.join(
            self.user_email_path, 'retrived.txt')

    def connect_and_greet(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((self.server, self.port))
        print(self.client_socket.recv(1024).decode('utf-8'))

    def send_commands(self):
        commands = [
            'CAPA',
            f'USER {self.username}',
            f'PASS {self.password}',
            'STAT'
        ]

        # Send commands
        for command in commands:
            self.client_socket.send(f'{command}\r\n'.encode('utf-8'))
            print(command)
            print("->", self.client_socket.recv(1024).decode('utf-8'))

    def get_email_index_list(self):
        self.client_socket.send(b'LIST\r\n')
        print("LIST")
        response = self.client_socket.recv(1024)
        print("->", response.decode('utf-8'))

        # get index in list
        self.index_list = [line.split(b' ')[0].decode('utf-8')
                           for line in response.split(b'\r\n')]
        # # eliminate char that is not num
        self.index_list = [int(num)
                           for num in self.index_list if num.isdigit()]

    def get_retr_list(self):
        with open(self.retrived_list_path, 'a+') as retr_file:
            retr_file.seek(0)
            retr_data = retr_file.read()
            if (len(retr_data) == 0):
                self.retr_list = self.index_list
            else:
                self.retr_list = []
                print("Init")
                retr_data = retr_data.split('\n')
                retr_data = retr_data[:len(retr_data) - 1]
                for element in self.index_list:
                    if str(element) not in retr_data:
                        self.retr_list.append(element)
                        print(element, "!!!!!!!!")
            retr_file.writelines(
                [f'{element}\n' for element in self.retr_list])

    def save_raw_email(self, element):
        # Create temporary text file to store raw email before parsing it
        raw_file_path = os.path.join(
            self.msg_folder_path, str(element) + ".msg")

        self.client_socket.send(f'RETR {element}\r\n'.encode('utf-8'))
        print("RETR", str(element)+"\n")
        with open(raw_file_path, 'ab') as file:
            while True:
                partial_response = self.client_socket.recv(1024)
                if not partial_response:
                    break
                file.write(partial_response)
                if b'\r\n.\r\n' in partial_response:
                    break

    def update_star_status(self, is_star, json_path):
        # Open the file and load its contents into a dictionary
        with open(json_path, "r") as file:
            data = json.load(file)

        # Change the value in the dictionary
        try:
            data["Star"] = str(is_star)
        except Exception as e:
            print(e)
        # Write the dictionary back to the file
        with open(json_path, "w") as file:
            json.dump(data, file)

    def filter(self, temp_message_path):
        print(os.path.join(temp_message_path, 'infor.json'))
        with open(os.path.join(temp_message_path, 'infor.json'), 'r') as file:
            data = json.load(file)

        try:
            with open(os.path.join(temp_message_path, 'content.txt'), 'r') as file:
                content = file.read()

            flag = False
            for key in FILTER.keys():
                if not flag:

                    for from_email in FILTER[key]["From"]:
                        if from_email in data["From"]:
                            if key == "Star":
                                self.update_star_status(True, os.path.join(temp_message_path, 'infor.json'))
                            shutil.move(temp_message_path, os.path.join(self.user_email_path, key))
                            flag = True
                            break

                    if not flag:
                        for sbj in FILTER[key]["Subject"]:
                            if sbj in data["Subject"]:
                                if key == "Star":
                                    self.update_star_status(True, os.path.join(temp_message_path, 'infor.json'))
                                shutil.move(temp_message_path, os.path.join(self.user_email_path, key))
                                flag = True
                                break

                        if not flag:
                            for c in FILTER[key]["Content"]:
                                if c in content:
                                    if key == "Star":
                                        self.update_star_status(True, os.path.join(temp_message_path, 'infor.json'))
                                    shutil.move(temp_message_path, os.path.join(self.user_email_path, key))
                                    flag = True
                                    break
            if not flag:
                shutil.move(temp_message_path, self.Inbox_path)
        except Exception as e:
            shutil.rmtree(temp_message_path)
            print(e)

    def quit_email(self):
        self.client_socket.send(b'QUIT\r\n')
        print(self.client_socket.recv(1024).decode('utf-8'))


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
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # get email info
    email_info = get_email_info(headers_dict)
    json_filename = 'infor.json'
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
        email_info.To = headers_dict.get('To', '').split(', ')
    except:
        email_info.To = ""

    try:
        email_info.Cc = headers_dict.get('Cc', '').split(', ')
    except:
        email_info.Cc = ""

    try:
        email_info.Bcc = headers_dict.get('Bcc', '').split(', ')
    except:
        email_info.Bcc = ""

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

    # print(part_headers_dict)

    # Check if the part in an attachment
    if 'attachment' in part_headers_dict.get('Content-Disposition', ''):
        # Extract filename and content
        # print(part_headers_dict.get('Content-Disposition', ''))
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
    # print(filename, "!!!")
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


def get_email(username, password, server, port):
    sample = receive_email(username, password, server, port)
    sample.connect_and_greet()
    sample.send_commands()
    sample.get_email_index_list()
    sample.get_retr_list()
    for element in sample.retr_list:
        print("Save", element)
        sample.save_raw_email(element)
    sample.quit_email()

    msg_paths = os.listdir(sample.msg_folder_path)
    for path in msg_paths:
        if int(path[:-4]) in sample.retr_list:
            with open(os.path.join(sample.msg_folder_path, path), 'rb') as file:
                parse_mime_structure(file.read().decode('utf-8'), int(path[:-4]), sample.user_email_path)

    for element in sample.retr_list:
        temp_message_path = os.path.join(sample.user_email_path, str(element))
        sample.filter(temp_message_path)


# if __name__ == '__main__':
#     get_email('clientserver@gmail.com', '12345678', "127.0.0.1", 2000)