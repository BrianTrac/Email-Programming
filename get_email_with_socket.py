import socket
import base64

def send_command(sock, command):
    sock.sendall((command + '\r\n').encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    print(response)
    return response

def get_messages(username, password, server, port=2000):
    try:
        # Connect to the server
        with socket.create_connection((server, port), timeout=5) as sock:
            response = sock.recv(1024).decode('utf-8')
            print(response)

            # Login to the server
            send_command(sock, f"USER {username}")
            send_command(sock, f"PASS {password}")

            # List available messages
            response = send_command(sock, "LIST")
            # Extract message IDs
            message_ids = [line.split()[0] for line in response.split('\n')[1:-2]]

            messages = []
            # Retrieve each message
            for message_id in message_ids:
                response = send_command(sock, f"RETR {message_id}")
                messages.append(response)

            return messages

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
username = 'clientserver@gmail.com'
password = '12345678'
server = '127.0.0.1'
messages = get_messages(username, password, server)

# Print the retrieved messages
for message in messages:
    print(message)
