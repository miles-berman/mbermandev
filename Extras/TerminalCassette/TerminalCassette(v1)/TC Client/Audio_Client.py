import pyaudio
import socket
import sys
import time
import threading

class AudioClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.file_path = None

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"\nConnected to {self.host}:{self.port}")

    def setup_audio_stream(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True,
            frames_per_buffer=1024
        )

    def set_file_path(self, path):
        self.file_path = path

    def send_file_path(self):
        while True:
            if self.client_socket and self.file_path:
                self.client_socket.send(self.file_path.encode('utf-8'))
                self.file_path = None
            time.sleep(1)

    def receive_and_play_audio(self):
        while True:
            data = self.client_socket.recv(512)
            if not data:
                break
            self.stream.write(data)

    def close_resources(self):
        print("\nStreaming finished.")
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'client_socket') and self.client_socket:
            self.client_socket.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()


    def start_client(self):
        while True:
            try:
                self.connect_to_server()
                self.setup_audio_stream()

                input_thread = threading.Thread(target=self.send_file_path)
                input_thread.daemon = True
                input_thread.start()

                self.receive_and_play_audio()

            except Exception as e:
                print(f"\nError occurred: {e}")
                self.close_resources()
                time.sleep(5)

            finally:
                self.close_resources()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5024
    client = AudioClient('192.168.0.40', port)
    client.start_client()
