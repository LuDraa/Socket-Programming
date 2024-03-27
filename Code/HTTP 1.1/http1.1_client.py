import socket
import os

# Define server address and port
SERVER_HOST = '10.154.17.153'  # IP address of the server
SERVER_PORT = 8000

# Specify the folder where files will be saved
folder_name = "B_10mb_received"

# Create the folder if it does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def request_and_save_file(repeat, file_name):
    for i in range(repeat):
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Send HTTP request to the server with the desired file name
        http_request = f"GET /{file_name} HTTP/1.1\r\nHost: localhost\r\n\r\n"
        client_socket.sendall(http_request.encode())

        # Receive HTTP response
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        # Close the connection
        client_socket.close()

        # Extract file content from HTTP response
        # Assuming the response follows the HTTP protocol, find the end of headers
        header_end = response.find(b"\r\n\r\n") + 4
        file_content = response[header_end:]

        # Define file path with unique identifier (i) within the specified folder
        file_path = os.path.join(folder_name, f"received_file_{i}")

        # Save the received file content to disk
        with open(file_path, "wb") as file:
            file.write(file_content)

    print(f"Requested and saved the file {repeat} times successfully in {folder_name}.")

if __name__ == "__main__":
    file_name = input("Enter the name of the file you want to request: ")  # Get the desired file name from user input
    request_and_save_file(1, file_name)