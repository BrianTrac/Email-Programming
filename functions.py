import pytz
import uuid
import os
import base64
from socket import *
from datetime import datetime, timedelta
import secrets

#function to generate a random boundary
def generate_boundary(length):
    return ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))

# Function to generate a unique message id
def generate_message_id():
    unique_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    message_id = f"<{unique_id}-{timestamp}@gmail.com>"
    return message_id

# Function to send simple message without attachment
def sendSimpleMessaage(client_socket, message):
    # Send Content-Type
    client_socket.send(
        f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'.encode('utf-8'))
    # Send Content-Transfer
    client_socket.send(
        f'Content-Transfer-Encoding: 7bit\r\n\r\n'.encode('utf-8'))
    # Send the email content
    email_content = f'{message}\r\n'
    client_socket.send(email_content.encode('utf-8'))

# function to send message with attachment
def sendMultipartMessage(client_socket, attachment_path, boundary):
    for path in attachment_path:
        client_socket.send(f'{boundary}\n'.encode('utf-8'))
        # Send Content-Type
        client_socket.send(f'Content-Type: text/plain; charset=UTF-8; name = "{os.path.basename(path)}"\r\n'.encode('utf-8'))
        # Send Content-Disposition
        client_socket.send(f'Content-Disposition: attachment; filename = "{os.path.basename(path)}"\r\n'.encode('utf-8'))
        # Send Content-Transfer
        client_socket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode('utf-8'))
        # Send the attachment content
        with open(path, "rb") as attachment:
            attachment_content = attachment.read()
            encoded_content = base64.b64encode(attachment_content).decode()
            client_socket.send(encoded_content.encode('utf-8'))
            client_socket.send('\r\n'.encode('utf-8'))
    client_socket.send(f'--{boundary}--\r\n'.encode('utf-8'))
    client_socket.send(f'.\r\n'.encode('utf-8'))

# Function to send email
def send_email(
        sender_name,
        sender_email,
        recipient_email,
        to_recipient_email,
        cc_recipient_email,
        bcc_recipient_email,
        subject,
        message,
        attachment_path):
    smtp_server = '127.0.0.1'
    smtp_port = 2225  # make sure that suits your server port

    # Your email credentials
    username = 'peter113@gmail.com'
    password = '12345678'

    # Create a socket connection
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((smtp_server, smtp_port))

    # Receive the server's greeting
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send the EHLO command
    client_socket.send('EHLO [127.0.0.1]\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send the MAIL FROM command
    client_socket.send(f'MAIL FROM: <{sender_email}>\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send the RCPT TO command
    for element in recipient_email:
        client_socket.send(f'RCPT TO: <{element}>\r\n'.encode('utf-8'))
        response = client_socket.recv(1024)
        print(response.decode('utf-8'))

    # Send the DATA command
    client_socket.send('DATA\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send the email headers
    if (attachment_path):
        # random string that never appears in the message
        boundary = generate_boundary(30)
        client_socket.send(f'Content-Type: multipart/mixed; boundary={boundary}\r\n'.encode('utf-8'))
    else:
        client_socket.send(f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'.encode('utf-8'))

    # Send Message-ID
    message_id = generate_message_id()
    client_socket.send(f'Message-ID: {message_id}\r\n'.encode('utf-8'))

    # Send Date
    timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(timezone).strftime("%a, %d %b %Y %H:%M:%S %z")
    client_socket.send(f'Date: {current_time}\r\n'.encode('utf-8'))

    # Send MIME-Version
    mime_version = "1.0"
    client_socket.send(f'MIME-Version: {mime_version}\r\n'.encode('utf-8'))

    # Send User-Agent
    user_agent = "Python"
    client_socket.send(f'User-Agent: {user_agent}\r\n'.encode('utf-8'))

    # Send Content-Language
    content_language = "en-US"
    client_socket.send(f'Content-Language: {content_language}\r\n'.encode('utf-8'))

    # Send To
    if to_recipient_email:
        to_rec_email = ', '.join(to_recipient_email)
        client_socket.send(f'To: {to_rec_email}\r\n'.encode('utf-8'))

    # Send CC
    if cc_recipient_email:
        cc_rec_email = ', '.join(to_recipient_email)
        client_socket.send(f'To: {cc_rec_email}\r\n'.encode('utf-8'))

    # Send if not people in To and CC
    if (not to_recipient_email) & (not cc_recipient_email):
        client_socket.send(f'To: undisclosed-recipients: ;\r\n'.encode('utf-8'))

    # Send From
    client_socket.send(f'From: {sender_name} <{sender_email}>\r\n'.encode('utf-8'))

    # Send Subject
    client_socket.send(f'Subject: {subject}\r\n'.encode('utf-8'))
    if attachment_path:
        client_socket.send(f'\r\nThis is multi-part message in MIME format.\n'.encode('utf-8'))
        client_socket.send(f'--{boundary}\n'.encode('utf-8'))
        sendSimpleMessaage(client_socket, message)
        sendMultipartMessage(client_socket, attachment_path,boundary)
    else:
        sendSimpleMessaage(client_socket, message)

    response = client_socket.recv(1024)
    print(response.decode('utf-8'))
    # Quit
    client_socket.send('QUIT\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Close the socket
    client_socket.close()
