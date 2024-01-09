from Tape_Storage import Library
from Audio_Server import AudioServer
from File_Server import FileServer
import threading

class TC_Server:
    def __init__(self, usrName="User"):
        self.Library = Library(usrName)

        self.AudioServer = AudioServer('0.0.0.0', 5024)
        self.FileServer = FileServer("0.0.0.0", 5025, self.Library)

        self.thread_init()

    def thread_init(self):
        server_thread = threading.Thread(target=self.AudioServer.start_server)
        server_thread.start()

        file_thread = threading.Thread(target=self.FileServer.start_server)
        file_thread.start()


