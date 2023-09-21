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

        # Receive and print the welcome message
        welcome_message = client_socket.recv(1024).decode()
        print(welcome_message)

        while True:
            # Prompt for registration or login
            action = input().strip()
            client_socket.sendall(action.encode())

            response = client_socket.recv(1024).decode()
            print(response)

            if response.startswith('Enter username'):
                username = input().strip()
                client_socket.sendall(username.encode())

                password = input().strip()
                client_socket.sendall(password.encode())

                registration_response = client_socket.recv(1024).decode()
                print(registration_response)

            elif response.startswith('Enter username'):
                username = input().strip()
                client_socket.sendall(username.encode())

                password = input().strip()
                client_socket.sendall(password.encode())

                login_response = client_socket.recv(1024).decode()
                print(login_response)

    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    start_client()
