import socket

def start_client():
    # Take user input for server address
    server_address = input('Enter server address (host:port): ').split(':')
    server_address = (server_address[0], int(server_address[1]))

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        while True:
            # Send a message to the server
            message = input('Enter a message to send to the server (or type "exit" to quit): ')
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode())

            # Receive and print the server's response
            response = client_socket.recv(1024)
            print(f'Received from server: {response.decode()}')
    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    start_client()
