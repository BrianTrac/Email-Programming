import pytz
import uuid
import os
from socket import *
from datetime import datetime, timedelta

RETR_FILE = "D:\\Python\\Socket Programming\\Email\\retr_file.txt"
CONTENT_EMAIL_FILE = "content_email.txt"
PATH = "D:\\Python\\Socket Programming\\Email\\Inbox"


def generate_message_id():
    unique_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    message_id = f"<{unique_id}-{timestamp}@gmail.com>"
    return message_id

def send_email(sender_name, sender_email, recipient_email, to_recipient_email, cc_recipient_email, bcc_recipient_email, subject, message):
    smtp_server = '127.0.0.1'
    smtp_port = 3000

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
        to_rec_email = ""
        for index, value in enumerate(to_recipient_email): 
            to_rec_email += value 
            if (index != len(to_recipient_email) - 1):
                to_rec_email += ', '

        client_socket.send(f'To: {to_rec_email}\r\n'.encode('utf-8'))

    # Send CC
    if cc_recipient_email:
        cc_rec_email = ""
        for index, value in enumerate(cc_recipient_email): 
            cc_rec_email += value 
            if (index != len(cc_recipient_email) - 1):
                cc_rec_email += ', '

        client_socket.send(f'CC: {cc_rec_email}\r\n'.encode('utf-8'))

    # Send if not people in To and CC
    if (not to_recipient_email) & (not cc_recipient_email):
        client_socket.send(f'To: undisclosed-recipients: ;\r\n'.encode('utf-8'))

    # Send From
    client_socket.send(f'From: {sender_name} <{sender_email}>\r\n'.encode('utf-8'))

    # Send Subject
    client_socket.send(f'Subject: {subject}\r\n'.encode('utf-8'))

    # Send Content-Type
    client_socket.send(f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'.encode('utf-8'))

    # Send Content-Transfer
    client_socket.send(f'Content-Transfer-Encoding: 7bit\r\n\r\n'.encode('utf-8'))

    # Send the email content
    email_content = f'{message}\r\n.\r\n'
    client_socket.send(email_content.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Quit
    client_socket.send('QUIT\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Close the socket
    client_socket.close()

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
            save_attachment(folder_path, filename, body)
    else:
        pass

def process_mime_structure(folder_path, part):
    # Extract headers and body for each part
    part_headers, part_body = part.split('\r\n\r\n', 1)

    # Parse headers into dictionary
    part_headers_dict = dict(line.split(": ", 1) for line in part_headers.split('\r\n') if ": " in line)

    # Check if the part in an attachment
    if 'attachment' in part_headers_dict.get('Content-Disposition', ''):
        # Extract filename and content
        filename = part_headers_dict.get('Content-Disposition', '').split('=')[1].strip('"')
        content = part_body.strip()
    else:
        filename = CONTENT_EMAIL_FILE
        content = part_body.strip()

    # Save to file
    save_attachment(folder_path, filename, content)

def save_attachment(folder_path, filename, content):
    # Combine the folder_path and filename
    file_path = os.path.join(folder_path, filename)

    # Open the file and write content to it
    with open(file_path, 'wb') as file:
        file.write(content.encode('utf-8'))

def receive_email(username, password):
    pop3_server = '127.0.0.1'
    pop3_port = 2000

    # Create a socket connection
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((pop3_server, pop3_port))

    # Receive the server's greeting
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send CAPA command
    client_socket.send(f'CAPA\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send USER command
    client_socket.send(f'USER {username}\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send PASS command
    client_socket.send(f'PASS {password}\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send STAT command
    client_socket.send(f'STAT\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Send LIST command
    client_socket.send(f'LIST\r\n'.encode('utf-8'))
    
    # Receive and print the initial part of the response
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
    index_list = [line.split(b' ')[0].decode('utf-8') for line in response.split(b'\r\n')] 
    # eliminate char that is not num
    index_list = [int(num) for num in index_list if num.isdigit()]


    # Send UIDL command
    client_socket.send(f'UIDL\r\n'.encode('utf-8'))

    # Receive and print the initial part of the response
    response = b''
    while True:
        partial_response = client_socket.recv(1024)
        if not partial_response:
            break
        response += partial_response
        if b'\r\n.\r\n' in partial_response:
            break
    print(response.decode('utf-8'))

    # Send RETR command
    with open (RETR_FILE, 'a+') as retr_file:
        retr_file.seek(0)
        retr_data = retr_file.read().split('\n')
        retr_list = index_list[len(retr_data):]
        for element in retr_list:
            client_socket.send(f'RETR {element}\r\n'.encode('utf-8'))
            retr_file.write(f'\n{element}')

            # Receive and print the initial part of the response
            response = b''
            while True:
                partial_response = client_socket.recv(1024)
                if not partial_response:
                    break
                response += partial_response
                if b'\r\n.\r\n' in partial_response:
                    break
            parse_mime_structure(response.decode('utf-8'), element)

    # Send QUIT command
    client_socket.send(f'QUIT\r\n'.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Close the socket
    client_socket.close()
    
# Example usage
sender_name = 'Thinh'
sender_email = 'peter113@gmail.com'
subject = 'Test Subject'
message = 'Hello, this is a Python agent.'

#to_email = 'clientserver@gmail.com dangphuchung321@gmail.com 22120120@student.hcmus.edu.vn'
to_email = ''
to_recipient_email = to_email.split(' ')

# Filter out empty strings
to_recipient_email = [email for email in to_recipient_email if email]

#cc_email_= 'clientserver@gmail.com dangphuchung321@gmail.com'
cc_email = ""
cc_recipient_email = cc_email.split(' ')

# Filter out empty strings
cc_recipient_email = [email for email in cc_recipient_email if email]

bcc_email = 'clientserver@gmail.com dangphuchung321@gmail.com 22120120@student.hcmus.edu.vn'
bcc_recipient_email = bcc_email.split(' ')

# Filter out empty strings
bcc_recipient_email = [email for email in bcc_recipient_email if email]

recipient_email = set(to_recipient_email) | set(cc_recipient_email) | set(bcc_recipient_email)

# send_email(sender_name, sender_email, recipient_email, to_recipient_email, cc_recipient_email, bcc_recipient_email, subject, message)

# Receiver info
username = 'clientserver@gmail.com'
password = '12345678'
receive_email(username, password)
