import os
import socket
import threading
from pydub import AudioSegment
from queue import Queue

class AudioServer:
    def __init__(self, host, port):
        self.stop_sending = threading.Event()
        self.audio_queue = Queue()
        self.flag = False
        self.host = host
        self.port = port
        self.client_socket = None
        self.client_connected = False

    def sanitize_path(self, path):
        path = path.replace("\ ", " ")
        path = path.replace("\\", "")
        return path


    # Check flag for new song
    def sending_check(self):
        if self.stop_sending.is_set():
            print("Stopping sending. Resetting loop.")
            self.stop_sending.clear()
            return True
        return False


    # Socket setup
    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        return server_socket

    # Accepting a client
    def accept_client(self, server_socket):
        server_socket.listen(1)
        self.client_socket, addr = server_socket.accept()
        return self.client_socket, addr

    # Preprocess Audio File
    def preprocess_audio(self, audio_file):
        audio = AudioSegment.from_file(audio_file)
        audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
        return audio.raw_data

    # Send Audio Data
    def send_audio_data(self, byte_data, chunk_size=512):
        print("Sending audio data...")
        self.audio_queue.queue.clear()
        for i in range(0, len(byte_data), chunk_size):
            if self.sending_check():
                return
            data_chunk = byte_data[i:i + chunk_size]
            self.client_socket.sendall(data_chunk)
        print("Done!\n")


    def get_path_from_client(self, buffer_size=1024):
        try:
            path_data = self.client_socket.recv(buffer_size)
            if path_data:
                path = path_data.decode('utf-8')
                return self.sanitize_path(path)
            else:
                print("No data received from the client.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        # Add this new method for cleanup
    def close_client(self):
        print("Closing client connection...")
        if self.client_socket:
            self.client_socket.close()
        self.client_socket = None
        self.flag = False
        self.audio_queue.queue.clear()
        self.stop_sending.clear()
        print("Closed.\n")
        
    def start_server(self):
        server_socket = self.create_server_socket()
        print(f"Listening on {self.host}:{self.port}...")

        while True:  # Add an outer loop to accept new clients
            self.client_connected = True
            client_socket, addr = self.accept_client(server_socket)
            print(f"Connection established with {addr}\n")

            path_thread = threading.Thread(target=self.get_audio_files)
            path_thread.start()

            while self.client_connected:
                if self.sending_check():
                    self.flag = False
                    continue

                if not self.audio_queue.empty():
                    audio_file = self.audio_queue.get()
                    print(f"Got audio file from queue: {audio_file}, Playing.\n")
                    byte_data = self.preprocess_audio(audio_file)
                    try:
                        self.send_audio_data(byte_data)
                    except BrokenPipeError as e:
                        print("Client disconnected...")
                        self.close_client()
                        break  # Break inner loop to accept a new client
                    
                    print(f"File {audio_file} sent.")


    def get_audio_files(self):
        global flag
        while True:
            audio_file = self.get_path_from_client()
            print("------------------")
            print(f"Recieved: {audio_file}")

            if not audio_file:
                self.client_connected = False
                break

            if self.flag:
                self.stop_sending.set()
            else:
                self.flag = True

            self.audio_queue.put(audio_file)
