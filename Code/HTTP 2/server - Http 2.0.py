import socket
import time
import os
import h2.connection
import h2.config
import numpy as np

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

def serve_file():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    config = h2.config.H2Configuration(client_side=False)
    conn = h2.connection.H2Connection(config=config)
    conn.initiate_connection()
    client_socket.sendall(conn.data_to_send())

    throughput_values = []
    total_data_transferred = 0
    start_time = time.time()

    try:
        while True:
            data = client_socket.recv(65535)
            if not data:
                break

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.RequestReceived):
                    transfer_start_time = time.time()

                    file_path = 'A_10kB'
                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                        file_size_bytes = len(file_content)

                    headers = [
                        (':status', '200'),
                        ('content-type', 'application/octet-stream'),
                        ('content-disposition', f'attachment; filename="{file_path}"')
                    ]
                    conn.send_headers(event.stream_id, headers)
                    conn.send_data(event.stream_id, file_content, end_stream=True)

                    transfer_end_time = time.time()
                    transfer_time = transfer_end_time - transfer_start_time
                    throughput = file_size_bytes / transfer_time
                    throughput_values.append(throughput)
                    total_data_transferred += file_size_bytes

            data_to_send = conn.data_to_send()
            if data_to_send:
                client_socket.sendall(data_to_send)

    finally:
        client_socket.close()

    total_transfer_time = time.time() - start_time

    if throughput_values:
        avg_throughput = sum(throughput_values) / len(throughput_values)
        throughput_std = np.std(throughput_values)
    else:
        avg_throughput = 0
        throughput_std = 0

    print(f"Total Data Transferred: {total_data_transferred} bytes")
    print(f"Total Transfer Time: {total_transfer_time} seconds")
    print(f"Average Throughput: {avg_throughput} bytes/second")
    print(f"Throughput Standard Deviation: {throughput_std} bytes/second")

if __name__ == "__main__":
    serve_file()
