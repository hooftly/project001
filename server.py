import socket
import threading
import signal
import sys

# Global variable to track whether the server should continue running
running = True

def handle_client(client_socket, client_address):
    print(f'Connection from {client_address}')

    while running:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break
        print(f'Received: {data.decode()}')

        # Send a response back to the client
        response = 'Hello, client! Thanks for connecting.'
        client_socket.sendall(response.encode())

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
