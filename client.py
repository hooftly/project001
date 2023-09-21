import socket
import hashlib
import sys

def hash_password(password):
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

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
        welcome_message_code = client_socket.recv(1)
        print("Welcome to the server!")

        while True:
            # Prompt for registration or login
            action = input("Register or Login? (Type '1' for register, '2' for login, 'exit' to quit): ").strip()

            if action == 'exit':
                break

            try:
                client_socket.sendall(bytes([int(action)]))
            except ValueError:
                print("Invalid input. Please enter '1' for register, '2' for login, or 'exit' to quit.")
                continue

            if action == '1':
                response_code = client_socket.recv(1)

                if response_code == b'\x01':
                    # Register a new user
                    print("Enter username:")
                    username = input().strip()
                    client_socket.sendall(username.encode())

                    print("Enter password:")
                    password = input().strip()
                    hashed_password = hash_password(password)
                    client_socket.sendall(hashed_password.encode())

                    registration_response_code = client_socket.recv(1)

                    if registration_response_code == b'\x01':
                        print("Registration successful! You are now logged in.")
                        print("Enter a message to send to the server (or type 'exit' to quit): ")

                        while True:
                            message = input().strip()
                            client_socket.sendall(message.encode())

                            if message == 'exit':
                                break
                    else:
                        print("Registration failed. Please try again.")
                else:
                    print("Server did not respond properly to registration request.")

            elif action == '2':
                response_code = client_socket.recv(1)

                if response_code == b'\x01':
                    # Login an existing user
                    print("Enter username:")
                    username = input().strip()
                    client_socket.sendall(username.encode())

                    print("Enter password:")
                    password = input().strip()
                    hashed_password = hash_password(password)
                    client_socket.sendall(hashed_password.encode())

                    login_response_code = client_socket.recv(1)

                    if login_response_code == b'\x01':
                        print(f"Welcome, {username}! You are logged in.")
                        print("Enter a message to send to the server (or type 'exit' to quit): ")

                        while True:
                            message = input().strip()
                            client_socket.sendall(message.encode())

                            if message == 'exit':
                                break
                    else:
                        print("Invalid username or password. Please try again.")
                else:
                    print("Server did not respond properly to login request.")

    finally:
        # Close the client socket
        client_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    start_client()
