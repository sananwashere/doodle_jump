# Import sockets, threading and pickle

import socket
import threading
import pickle

# Define server parameters
SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 1237
BUFFER_SIZE = 4096

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

# Lists to store client sockets and player data
client_sockets = []
player_data = {}

# Locks for thread safety
client_sockets_lock = threading.Lock()
player_data_lock = threading.Lock()

# Function to handle communication with each client
def handle_client(client_socket):
    try:
        # Set timeout for receiving data
        client_socket.settimeout(60)
        while True:
            # Receive data from client
            data = client_socket.recv(BUFFER_SIZE)

            # If no data is received, the client has disconnected
            if not data:
                break

            # Deserialize received pickle data
            received_data = pickle.loads(data)

            # Broadcast the received data to all other clients
            with client_sockets_lock:
                for client in client_sockets:
                    # Don't send data back to the sender
                    if client != client_socket:
                        try:
                            # Send data to other clients
                            client.send(pickle.dumps(received_data))
                        except socket.error as e:
                            print(f"Error sending data to {client}: {e}")
    except (socket.error, EOFError, pickle.UnpicklingError, socket.timeout) as e:
        print(f"Error in communication with {client_socket}: {e}")
    finally:
        # Close client socket
        with client_sockets_lock:
            client_sockets.remove(client_socket)
        client_socket.close()

# Main loop to accept incoming connections
try:
    while True:
        # Accept new client connection
        client_socket, address = server_socket.accept()
        with client_sockets_lock:
            # Add client socket to the list
            client_sockets.append(client_socket)

        print(f"Connection from {address} established.")

        # Send initial player_info to the newly connected client
        with player_data_lock:
            # Get player_info for the new client
            player_info = player_data.get(client_socket)


        # Send player_info to the client
        client_socket.send(pickle.dumps(player_info))

        # Create a new thread to handle communication with the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()  # Start the thread to handle client communication

except KeyboardInterrupt:
    print("Server is shutting down.")
finally:
    # Close the server socket
    server_socket.close()




