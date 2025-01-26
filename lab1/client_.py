import socket
import threading


class Client:
    def __init__(self):
        self.ip = '192.168.118.238'
        self.port = 12345

    @staticmethod
    def listen_for_messages(client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    print("Server connection closed.")
                    break
                print(f"\n{data}")
            except ConnectionError:
                print("Error: Lost connection to the server.")
                break

    def start_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.ip, self.port))
            print(f"Connected to server at {self.ip}:{self.port}")

            threading.Thread(target=self.listen_for_messages, args=(client_socket,), daemon=True).start()

            while True:
                message = input()
                if message.lower() == 'exit':
                    print("Disconnecting from the server.")
                    break
                client_socket.send(message.encode())