import libtorrent as lt
import sys
import os
import time
import statistics

def setup_session(torrent_file):
    session = lt.session()
    torrent_info = lt.torrent_info(torrent_file)
    return session.add_torrent({'ti': torrent_info, 'save_path': '.'})

def download_file(torrent_handle, target_file):
    start_time = time.time()
    if os.path.exists(target_file):
        os.remove(target_file)
    
    while not torrent_handle.is_seed():
        s = torrent_handle.status()
        print(f'\r{s.progress * 100:.2f}% complete (down: {s.download_rate / 1000:.1f} kB/s up: {s.upload_rate / 1000:.1f} kB/s peers: {s.num_peers}) {s.state}', end=' ')
        time.sleep(1)
    
    return time.time() - start_time

def main(torrent_file):
    file_size_list = []
    target_file = './A_1mB'  # Assuming the file to download is 'A_10MB'
    torrent_handle = setup_session(torrent_file)
    download_time = download_file(torrent_handle, target_file)
    file_size = os.path.getsize(target_file)
    throughput = file_size / download_time
    file_size_list.append(throughput)
    
    print(f'\nDownload complete! Throughput: {throughput:.2f} bytes/sec')
    print(f'Mean throughput: {statistics.mean(file_size_list):.2f} bytes/sec')
    if len(file_size_list) > 1:
        print(f'Standard deviation: {statistics.stdev(file_size_list):.2f}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python downloader.py <torrent file>")
    else:
        main(sys.argv[1])
