import socket
import threading
from Tape_Storage import Library

class FileServer:

    def __init__(self, host, port, usrLibrary):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.library = usrLibrary

        self.command_map = {
            "GET_COLLECTIONS": self.get_collections,
            "GET_CASSETTES": self.get_cassettes,
            "GET_TRACKS": self.get_tracks
        }

    def get_collections(self, _, client_socket):
        collections = self.library.Collections()
        for col in collections:
            client_socket.send((col.title + "\n").encode('utf-8'))

    def get_cassettes(self, choice, client_socket):
        cassettes = self.library.Cassettes(choice)
        for cas in cassettes:
            client_socket.send((cas.title + "\n").encode('utf-8'))

    def get_tracks(self, choice, client_socket):
        tracks = self.library.Tracks(choice)
        for track in tracks:
            data = track.title + ">" + track.path
            client_socket.send((data + "\n").encode('utf-8'))

    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        return server_socket

    def accept_client(self, server_socket):
        server_socket.listen(1)
        self.client_socket, addr = server_socket.accept()
        return self.client_socket, addr

    def handle_client(self, client_socket):
        try:
            while True:
                print("Waiting for client request...")
                request = client_socket.recv(1024).decode('utf-8')
                
                if not request:
                    print("Client disconnected.")
                    break

                print("Processing client request...")
                self.handle_input(request, client_socket)
                client_socket.sendall("<END>".encode('utf-8'))

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            print("Closing client connection...")
            client_socket.close()
            print("Closed.\n")

    def handle_input(self, request, client_socket):
        try:
            command, args = request.split(":")
            func = self.command_map.get(command)
            if func:
                print(f"Executing command: {command}")
                func(args, client_socket)
            else:
                print("Invalid command received.")
                client_socket.send("INVALID COMMAND\n".encode('utf-8'))

        except ValueError:  
            func = self.command_map.get(request)
            if func:
                print(f"Executing command: {request}")
                func(None, client_socket)
            else:
                print("Invalid command received.")
                client_socket.send("INVALID COMMAND\n".encode('utf-8'))

    def start_server(self):
        self.server_socket = self.create_server_socket()
        print(f"Listening on {self.host}:{self.port}...")

        try:
            while True:
                print("Waiting for a new connection...")
                client_socket, addr = self.accept_client(self.server_socket)
                print(f"Connection established with {addr}\n")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()

        except KeyboardInterrupt:
            print("Shutting down the server.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            print("Closing server socket...")
            self.server_socket.close()
            print("Closed.\n")
