import socket
import threading

class Client:
    def __init__(self, server_host="127.0.0.1", server_port=12345):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind(("", 0))
        self.local_address = self.client_socket.getsockname()

    def receive_messages(self):
        """
        Continuously listens for incoming messages from the server.
        """
        while True:
            try:
                data, addr = self.client_socket.recvfrom(1024)
                print(f"\n{data.decode()}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_messages(self):
        """
        Continuously sends user input to the server.
        """
        print(f"Connected to server at {self.server_host}:{self.server_port}. Type 'exit' to quit.")
        print(f"To send a private message, use the format: /pm <ip>:<port> <message>")

        while True:
            try:
                message = input()
                if message.lower() == "exit":
                    print("Exiting...")
                    break
                self.client_socket.sendto(message.encode(), (self.server_host, self.server_port))
            except Exception as e:
                print(f"Error sending message: {e}")
                break

    def run(self):
        """
        Starts the client's send and receive threads.
        """
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.send_messages()

