from concurrent import futures
import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
import os
import time
import statistics

class FileTransferService(file_transfer_pb2_grpc.FileTransferServiceServicer):
    def __init__(self):
        self.throughputs = []

    def TransferFile(self, request, context):
        filename = request.filename
        chunk_size = 1024  # You might adjust chunk size as needed
        file_path = os.path.join(os.getcwd(), filename)  # Adjust the path to your files
        
        if not os.path.exists(file_path):
            context.set_details(f"File '{filename}' not found.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return file_transfer_pb2.FileChunk()

        start_time = time.time()
        total_bytes_sent = 0
        with open(file_path, 'rb') as file:
            while True:
                piece = file.read(chunk_size)
                if not piece:
                    break
                yield file_transfer_pb2.FileChunk(content=piece)
                total_bytes_sent += len(piece)

        end_time = time.time()
        transfer_time = end_time - start_time
        throughput = total_bytes_sent / transfer_time
        self.throughputs.append(throughput)

        if len(self.throughputs) == 10:
            average_throughput = sum(self.throughputs) / len(self.throughputs)
            std_dev_throughput = statistics.stdev(self.throughputs)
            print(f"Average Throughput after 10 files: {average_throughput} bytes per second")
            print(f"Standard Deviation of Throughput after 10 files: {std_dev_throughput} bytes per second")
            self.throughputs.clear()  # Clear the list for the next set of 1000 files

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServiceServicer_to_server(FileTransferService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at [::]:50051.")
    try:
        while True:
            time.sleep(3600)  # 1 hour
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
