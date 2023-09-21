import socket
import threading
import signal
import sys

# Global variable to track whether the server should continue running
running = True

# Dictionary to store user accounts (username: User object)
user_accounts = {}

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def handle_client(client_socket, client_address):
    global user_accounts

    print(f'Connection from {client_address}')

    # Send a welcome message and prompt for registration
    client_socket.sendall(b'\x01')  # 0x01 indicates welcome message
    client_socket.sendall(b'\x01')  # 0x01 indicates registration/login prompt

    while running:
        try:
            # Receive data from the client
            message_type = client_socket.recv(1)

            if message_type == b'\x01':
                # Register a new user
                client_socket.sendall(b'\x01')  # 0x01 indicates enter username
                username = client_socket.recv(1024).decode().strip()

                client_socket.sendall(b'\x01')  # 0x01 indicates enter password
                password = client_socket.recv(1024).decode().strip()

                user_accounts[username] = User(username, password)
                client_socket.sendall(b'\x01')  # 0x01 indicates registration successful

                # Start processing messages from the client after successful registration
                while True:
                    message = client_socket.recv(1024)
                    if not message:
                        break
                    print(f'Received from {username}: {message.decode()}')

            elif message_type == b'\x02':
                # Login an existing user
                client_socket.sendall(b'\x01')  # 0x01 indicates enter username
                username = client_socket.recv(1024).decode().strip()

                client_socket.sendall(b'\x01')  # 0x01 indicates enter password
                password = client_socket.recv(1024).decode().strip()

                if username in user_accounts and user_accounts[username].password == password:
                    client_socket.sendall(b'\x01')  # 0x01 indicates successful login

                    while True:
                        # Send data in chunks of 1024 bytes after successful login
                        message = client_socket.recv(1024)
                        if not message:
                            break
                        print(f'Received from {username}: {message.decode()}')

                else:
                    client_socket.sendall(b'\x00')  # 0x00 indicates failed login

            else:
                client_socket.sendall(b'\x00')  # 0x00 indicates invalid input

        except ConnectionResetError:
            print(f'Connection with {client_address} reset by peer.')
            break

    # Close the client socket
    client_socket.close()
    print(f'Connection with {client_address} closed.')

def sigint_handler(signal, frame):
    global running
    running = False
    print("\nShutting down server...")
    server_socket.close()
    sys.exit(0)

# Take user input for server address
server_address = input('Enter server address (host:port): ').split(':')
server_address = (server_address[0], int(server_address[1]))

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

print(f'Server is listening on {server_address[0]}:{server_address[1]}...')

# Set up the signal handler for Ctrl+C
signal.signal(signal.SIGINT, sigint_handler)

while running:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
