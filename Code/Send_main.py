import pytz
import uuid
import os
import base64
from socket import *
from datetime import datetime, timedelta, timezone
import secrets
import mimetypes
import shutil
import json

smtp_server = '127.0.0.1'
smtp_port = 2225


class EmailInfo:
    def __init__(self, Date=None,From=None, To=None, Cc=None, Bcc=None, Subject=None, message=None):
        self.Date = Date
        self.From = From   
        self.To = To
        self.Cc = Cc
        self.Bcc = Bcc
        self.Subject = Subject
        self.message = message

    def to_dict(self):
        return {
            'Date': self.Date,
            'From': self.From,
            'To': self.To,
            'Cc': self.Cc,
            'Bcc': self.Bcc,
            'Subject': self.Subject
        }

    def save_to_json(self, obj, filename):
        with open(filename, 'w') as file:
            json.dump(obj.to_dict(), file)

#####################################################################################################


class SendEmail:
    def __init__(self, sender_name, sender_email, to_email, cc_email, bcc_email, subject, message, attachment_path, EmailInfo):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.to_email = to_email.split(' ')
        self.cc_email = cc_email.split(' ')
        self.bcc_email = bcc_email.split(' ')
        self.subject = subject
        self.message = message
        self.attachment_path = attachment_path
        self.recipient_email = set(self.to_email) | set(
            self.cc_email) | set(self.bcc_email)
        self.boundary = ''
        self.emailInfor = EmailInfo()

        self.smtp_server = '127.0.0.1'
        self.smtp_port = 2225

        


    def connect_server(self):
        # Create a socket connection
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((smtp_server, smtp_port))
        # Receive the server's greeting
        response = self.client_socket.recv(1024)
        print(response.decode('utf-8'))
        
    def send_command(self):

        # Send the EHLO command
        self.client_socket.send('EHLO [127.0.0.1]\r\n'.encode('utf-8'))
        response = self.client_socket.recv(1024)
        print(response.decode('utf-8'))

        # Send the MAIL FROM command
        self.client_socket.send(
            f'MAIL FROM:<{self.sender_email}>\r\n'.encode('utf-8'))
        response = self.client_socket.recv(1024)
        print(response.decode('utf-8'))

        # Send the RCPT TO command
        for element in self.recipient_email:
            self.client_socket.send(f'RCPT TO:<{element}>\r\n'.encode('utf-8'))
            response = self.client_socket.recv(1024)
            print(response.decode('utf-8'))

        # Send the DATA command
        self.client_socket.send('DATA\r\n'.encode('utf-8'))
        response = self.client_socket.recv(1024)
        print(response.decode('utf-8'))

    def generate_message_id():
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        message_id = f"<{unique_id}-{timestamp}@gmail.com>"
        return message_id

    def send_email_headers(self):
        # Send the email headers
        if self.attachment_path:
            # random string that never appears in the message
            self.boundary = secrets.token_hex(16)
            self.client_socket.send(
                f'Content-Type: multipart/mixed; boundary="{self.boundary}"\r\n'.encode('utf-8'))
        else:
            self.client_socket.send(
                f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'.encode('utf-8'))

    def send_id(self):
        # Send Message-ID
        message_id = self.generate_message_id()
        self.client_socket.send(
            f'Message-ID: {message_id}\r\n'.encode('utf-8'))

    def send_date(self):
        # Send Date
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        self.current_time = datetime.now(timezone).strftime(
            "%a, %d %b %Y %H:%M:%S %z")
        self.client_socket.send(
            f'Date: {self.current_time}\r\n'.encode('utf-8'))

    def send_mime_version(self):
        # Send MIME-Version
        mime_version = "1.0"
        self.client_socket.send(
            f'MIME-Version: {mime_version}\r\n'.encode('utf-8'))

    def get_mime_type(file_path):
        return mimetypes.guess_type(file_path)[0]

    def send_user_agent(self):
        # Send User-Agent
        user_agent = "Python"
        self.client_socket.send(
            f'User-Agent: {user_agent}\r\n'.encode('utf-8'))

    def send_content_language(self):
        # Send Content-Language
        content_language = "en-US"
        self.client_socket.send(
            f'Content-Language: {content_language}\r\n'.encode('utf-8'))

    def send_to_recipient(self):
        # Send To
        if self.to_email:
            to_rec_email = ', '.join(self.to_email)
            self.client_socket.send(f'To: {to_rec_email}\r\n'.encode('utf-8'))

        # Send CC
        if self.cc_email:
            cc_rec_email = ', '.join(self.cc_email)
            self.client_socket.send(f'Cc: {cc_rec_email}\r\n'.encode('utf-8'))

        # Send if not people in To and CC
        if (not self.to_email) & (not self.cc_email):
            self.client_socket.send(
                f'To: undisclosed-recipients: ;\r\n'.encode('utf-8'))

        # Send From
        self.client_socket.send(f'From: {self.sender_name} <{self.sender_email}>\r\n'.encode('utf-8'))
        # Send Subject
        self.client_socket.send(f'Subject: {self.subject}\n'.encode('utf-8'))

    def send_content(self):
        if self.attachment_path:
            self.client_socket.send(
                f'\r\nThis is a multi-part message in MIME format.\r\n'.encode('utf-8'))
            self.client_socket.send(f'--{self.boundary}\r\n'.encode('utf-8'))

            # Send Content-Type
            self.client_socket.send(
                f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'.encode('utf-8'))
            # Send Content-Transfer
            self.client_socket.send(
                f'Content-Transfer-Encoding: 7bit'.encode('utf-8'))
            # Send the email content
            email_content = f'\r\n\r\n{self.message}\r\n\r\n'
            self.client_socket.send(email_content.encode('utf-8'))

            for path in self.attachment_path:

                self.client_socket.send(f'--{self.boundary}\n'.encode('utf-8'))
                # Send Content-Type
                self.client_socket.send(f'Content-Type: {self.get_mime_type(path)}; charset=UTF-8; name="{os.path.basename(path)}"\r\n'.encode('utf-8'))
                # Send Content-Disposition
                self.client_socket.send(f'Content-Disposition: attachment; filename="{os.path.basename(path)}"\r\n'.encode('utf-8'))
                # Send Content-Transfer
                self.client_socket.send(
                    f'Content-Transfer-Encoding: base64\r\n\r\n'.encode('utf-8'))
                # Send the attachment content
                with open(path, "rb") as attachment:
                    attachment_content = attachment.read()
                    encoded_content = base64.b64encode(
                        attachment_content).decode()
                    # Split the content into lines of a maximum length, for
                    # example, 998 characters
                    lines = [encoded_content[i:i + 998]
                             for i in range(0, len(encoded_content), 998)]
                    # Send each line separately
                    for line in lines:
                        self.client_socket.send(
                            (line + '\r\n').encode('utf-8'))
            # end of the multipart message
            self.client_socket.send(
                f'\r\n\r\n--{self.boundary}--\r\n\r\n'.encode('utf-8'))
        else:
            # Send Content-Type
            self.client_socket.send(
                f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'.encode('utf-8'))
            # Send Content-Transfer
            self.client_socket.send(
                f'Content-Transfer-Encoding: 7bit\r\n\r\n'.encode('utf-8'))
            # Send the email content
            email_content = f'{self.message}\r\n\r\n'
            self.client_socket.send(email_content.encode('utf-8'))

        self.client_socket.send('.\r\n'.encode('utf-8'))  # end of the data section
        response = self.client_socket.recv(1024)
        print(response.decode('utf-8'))

    def close_connect(self):
        # Quit
        self.client_socket.send('QUIT\r\n.'.encode('utf-8'))
        response = self.client_socket.recv(1024)
        print(response.decode('utf-8'))

        # Close the socket
        self.client_socket.close()

    def store_sent_email(self):

        current_folder = os.path.dirname(os.path.abspath(__file__))
        sent_folder_path = os.path.join(current_folder, 'Sent_Items')
        # Check if the directory does not exist before trying to create it
        if not os.path.exists(sent_folder_path):
            os.mkdir(sent_folder_path)

        items_in_directory = os.listdir(sent_folder_path)

        # Filter the list to only include subdirectories
        subdirectories = [item for item in items_in_directory if os.path.isdir(
            os.path.join(sent_folder_path, item))]

        current_items = len(subdirectories)
        email_folder_path = os.path.join(
            sent_folder_path, str(current_items+1))

        # Check if the directory does not exist before trying to create it
        if not os.path.exists(email_folder_path):
            os.mkdir(email_folder_path)

        # Date
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.now(timezone).strftime(
            "%a, %d %b %Y %H:%M:%S %z")

        emailInfor = EmailInfo(
            self.current_time,
            self.sender_email,
            self.to_email,
            self.cc_email,
            self.bcc_email,
            self.subject,
            self.message)

        infor_path = os.path.join(email_folder_path, "infor.json")
        emailInfor.save_to_json(emailInfor, infor_path)

        content_path = os.path.join(email_folder_path, "content.txt")
        with open(content_path, 'w') as file:
            file.write(self.message)

        for path in self.attachment_path:
            shutil.copy(path, email_folder_path)






def send(sender_name, sender_email, to_email, cc_email, bcc_email, subject, message, attachment_path):
    send_email = SendEmail
    send_email.__init__(send_email, sender_name, sender_email, to_email, cc_email, bcc_email, subject, message, attachment_path, EmailInfo)
    send_email.connect_server(send_email)
    send_email.send_command(send_email)
    send_email.send_email_headers(send_email)
    send_email.send_id(send_email)
    send_email.send_date(send_email)
    send_email.send_mime_version(send_email)
    send_email.send_user_agent(send_email)
    send_email.send_content_language(send_email)
    send_email.send_to_recipient(send_email)
    send_email.send_content(send_email)
    send_email.close_connect(send_email)
    send_email.store_sent_email(send_email)
    
# send(
#     "Anh Khoa",
#     "anhkhoa@gmail.com",
#     "kiin@gmail.com",
#     "test@gmail.com",
#     "bcc@gmail.com",
#     "subject",
#     "message",
#     [])
