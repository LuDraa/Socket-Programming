import grpc
import file_pb2
import file_pb2_grpc

def send_file(file_content):
    channel = grpc.insecure_channel('localhost:50051')
    stub = file_pb2_grpc.FileTransferStub(channel)
    response = stub.SendFile(file_pb2.FileRequest(file_content=file_content))
    print("Response:", response.message)

if __name__ == '__main__':
    # Read file content from file A_10kB
    with open('A_10MB', 'rb') as file:
        file_content = file.read()
    send_file(file_content)