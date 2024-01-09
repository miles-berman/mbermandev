import threading
import socket
import time
import os
from Audio_Client import AudioClient  # Replace with the actual import
from PyInquirer import prompt, Separator

class LibraryTerminalApp:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reconnect()
        self.currentCassette = ""
        self.currentTrack = ""

        audio_port = 5024
        self.audio_client = AudioClient('192.168.0.40', audio_port)
        audio_client_thread = threading.Thread(target=self.audio_client.start_client)
        audio_client_thread.daemon = True
        audio_client_thread.start()

    def send_request(self, request):
        try:
            self.client.send(request.encode('utf-8'))

            buffer = []
            while True:
                part = self.client.recv(1024).decode('utf-8')
                if "<END>" in part:
                    buffer.append(part.split("<END>")[0])
                    break
                buffer.append(part)

            full_response = "".join(buffer)
            return full_response.strip().split('\n')

        except (ConnectionResetError, BrokenPipeError):
            os.system('clear')  # Clear the terminal
            print("Connection was lost. Attempting to reconnect.")
            self.reconnect()
            return []  # Returning an empty list to signify failure

    def reconnect(self):
        os.system('clear')  # Clear the terminal
        self.client = None
        while self.client is None:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((self.host, self.port))
            except ConnectionRefusedError:
                print("Connection refused. Retrying in 5 seconds...")
                time.sleep(5)

    def ask_question(self, message, choices, back_option=False):
        question_choices = choices.copy()

        if back_option:
            question_choices.append(Separator())
            question_choices.append("<-")

        questions = [
            {
                'type': 'list',
                'name': 'selection',
                'message': message,
                'choices': question_choices
            }
        ]
        os.system('clear')
        self.menuBar()
        answer = prompt(questions)
        return answer.get('selection', 'Exit')

    def menuBar(self):
        print("\033[1;33m" + "=" * 35 + "\033[0m")
        cassetteStr = f"""\033[1;32m
.------------------------.
|\\////////       90 min  |
| \/  __  ______  __     |
|    /  \|\.....|/  \    |\033[0m  {self.currentTrack} \033[1;32m
|    \__/|/_____|\__/    |\033[0m  {self.currentCassette} \033[1;32m                                             
| A                      |                                                
|    ________________    |                                                
|___/_._o________o_._\___|

\033[0m"""
        print(cassetteStr)
        print("\033[1;33m" + "=" * 35 + "\033[0m")

    def run(self):
        try:
            while True:
                collections = self.send_request("GET_COLLECTIONS:")
                
                if not collections:
                    continue  # Retry
                
                collection_choice = self.ask_question("Select a collection:", collections)

                if collection_choice == '<-':
                    break

                cassettes = self.send_request(f"GET_CASSETTES:{collection_choice}")
                
                if not cassettes:
                    continue  # Retry
                
                while True:
                    cassette_choice = self.ask_question("Select a cassette:", cassettes, back_option=True)

                    if cassette_choice == '<-':
                        break

                    tracks = self.send_request(f"GET_TRACKS:{cassette_choice}")
                    
                    if not tracks:
                        break  # Break out of the track loop and go back to cassettes

                    track_titles = [track.split(">")[0] for track in tracks]
                    while True:
                        track_choice = self.ask_question("Select a track:", track_titles, back_option=True)


                        if track_choice == '<-':
                            break
                        else:
                            self.currentTrack = track_choice
                            self.currentCassette = cassette_choice
                            selected_track = tracks[track_titles.index(track_choice)]
                            track_path = selected_track.split(">")[1]
                            self.audio_client.set_file_path(track_path)
        finally:
            self.client.close()


if __name__ == "__main__":
    app = LibraryTerminalApp('192.168.0.104', 5025)
    app.run()
