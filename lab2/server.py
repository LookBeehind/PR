import socket

class Server:
    def __init__(self, host="0.0.0.0", port=12345):
        self.host = host
        self.port = port
        self.clients = set()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        print(f"UDP server listening on {self.host}:{self.port}")

    def run(self):
        """
        Main loop to receive and broadcast/private messages.
        """
        while True:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                message = data.decode()

                if addr not in self.clients:
                    self.clients.add(addr)
                    print(f"New client added: {addr}")

                if message.startswith("/pm"):
                    # Format: /pm <ip>:<port> <message>
                    try:
                        parts = message.split(" ", 2)
                        if len(parts) < 3:
                            # If the message format is incomplete
                            error_msg = "Invalid /pm format. Use: /pm <ip>:<port> <message>"
                            self.server_socket.sendto(error_msg.encode(), addr)
                            print(f"Invalid private message format from {addr}: {message}")
                            continue

                        _, recipient, private_msg = parts
                        recipient_ip, recipient_port = recipient.split(":")
                        recipient_addr = (recipient_ip, int(recipient_port))

                        if recipient_addr in self.clients:
                            private_message = f"Private message from {addr}: {private_msg}"
                            self.server_socket.sendto(private_message.encode(), recipient_addr)
                            print(f"Private message sent from {addr} to {recipient_addr}")
                        else:
                            error_msg = f"Error: Client {recipient_addr} not found."
                            self.server_socket.sendto(error_msg.encode(), addr)
                    except ValueError:
                        error_msg = "Invalid /pm format. Use: /pm <ip>:<port> <message>"
                        self.server_socket.sendto(error_msg.encode(), addr)
                        print(f"Error processing private message from {addr}: {message}")
                else:
                    broadcast_message = f"Public message from {addr}: {message}"
                    print(broadcast_message)
                    for client in self.clients:
                        if client != addr:
                            self.server_socket.sendto(broadcast_message.encode(), client)

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    server = Server()
    server.run()
