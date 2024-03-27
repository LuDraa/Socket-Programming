import socket
import time
import numpy as np

# Define server address and port
SERVER_HOST = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 8000

def serve_file():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    # Initialize lists to store throughput values
    throughput_values = []
    total_data_transferred = 0
    t1_start_time = time.time()
    # Loop for file transfers
    for _ in range(1):
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Record start time for each transfer
        transfer_start_time = time.time()

        # Read HTTP request from the client
        request = client_socket.recv(1024).decode()

        # Extract requested file name from the HTTP request
        requested_file = request.split()[1][1:]  # Extracts the requested file name from the HTTP request
        
        # Respond with the requested file content
        with open(requested_file, 'rb') as file:  # Open the requested file
            file_content = file.read()

        # HTTP response header
        response = f"""HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="{requested_file}"

"""

        # Send HTTP response header and file content
        client_socket.sendall(response.encode() + file_content)

        # Record end time for each transfer
        transfer_end_time = time.time()

        # Calculate time taken for transfer
        transfer_time = transfer_end_time - transfer_start_time

        # Calculate throughput during this transfer
        file_size_bytes = len(file_content)
        transfer_throughput = file_size_bytes / transfer_time

        # Append throughput to list
        throughput_values.append(transfer_throughput)

        # Update total data transferred
        total_data_transferred += file_size_bytes

        # Close the connection
        client_socket.close()

    t2_stop_time = time.time()
    # Calculate total transfer time
    total_transfer_time = t2_stop_time - t1_start_time
    print("total", total_transfer_time)


    # Calculate average throughput
    if throughput_values:
        avg_throughput = sum(throughput_values) / len(throughput_values)
    else:
        avg_throughput = 0

    # Calculate standard deviation of throughput
    throughput_std = np.std(throughput_values) if throughput_values else 0

    print(f"Average Throughput: {avg_throughput} bytes/second")
    print(f"Throughput Standard Deviation: {throughput_std} bytes/second")

if __name__ == "__main__":
    serve_file()
