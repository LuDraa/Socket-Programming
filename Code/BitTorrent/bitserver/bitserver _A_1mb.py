import libtorrent as lt
import time
import os

def create_session():
    return lt.session()

def create_or_verify_torrent_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("A_1mb.")

def add_file_to_session(session, file_path):
    torrent_info = lt.torrent_info(file_path)
    return session.add_torrent({'ti': torrent_info, 'save_path': '.'})

def main():
    session = create_session()
    torrent_file = "./ape.torrent"
    create_or_verify_torrent_file(torrent_file)
    torrent_handle = add_file_to_session(session, torrent_file)
    
    print('Sharing:', torrent_handle.name())
    
    try:
        while True:
            time.sleep(10)  # Seed indefinitely
    except KeyboardInterrupt:
        print('\nSeeder stopped.')

if __name__ == "__main__":
    main()
