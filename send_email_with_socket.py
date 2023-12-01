import pytz
import uuid
from socket import *
from datetime import datetime, timedelta


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

send_email(sender_name, sender_email, recipient_email, to_recipient_email, cc_recipient_email, bcc_recipient_email, subject, message)


