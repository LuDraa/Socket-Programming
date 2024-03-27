import os
import socket
import h2.connection
import h2.config

SERVER_HOST = '10.154.17.153'  # Update this to your server's IP address
SERVER_PORT = 8000

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    config = h2.config.H2Configuration(client_side=True)
    conn = h2.connection.H2Connection(config=config)
    conn.initiate_connection()
    client_socket.sendall(conn.data_to_send())

    # Adjust the loop to ensure odd stream IDs are used
    for i in range(1,2,2):  # Start from 1, increment by 2, up to 2000 to ensure odd IDs
        headers = [
            (':method', 'GET'),
            (':scheme', 'http'),
            (':path', '/'),
            (':authority', f'{SERVER_HOST}:{SERVER_PORT}'),
            ('user-agent', 'hyper-h2/1.0.0')
        ]
        conn.send_headers(i, headers, end_stream=True)
        client_socket.sendall(conn.data_to_send())

        folder_path = "HTTP2_B_10MB_received"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, f"B_10MB_{i}")
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(65535)
                if not data:
                    break

                events = conn.receive_data(data)
                for event in events:
                    if isinstance(event, h2.events.DataReceived):
                        file.write(event.data)
                        conn.acknowledge_received_data(event.flow_controlled_length, event.stream_id)

                data_to_send = conn.data_to_send()
                if data_to_send:
                    client_socket.sendall(data_to_send)

                if any(isinstance(e, h2.events.StreamEnded) for e in events):
                    print(f"File B_10MB_{i} received")
                    break  # Exit the loop once the stream ends

    client_socket.close()

if __name__ == "__main__":
    main()
