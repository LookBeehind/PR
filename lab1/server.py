import socket
import threading

clients = []
conversation_history = []

def broadcast_message(message, sender_conn=None):
    for client in clients:
        conn, _ = client
        if conn != sender_conn:
            try:
                conn.send(message.encode())
            except ConnectionError:
                clients.remove(client)

def handle_client(conn, addr):
    global conversation_history
    print(f"New connection from {addr}")
    with conn:
        if conversation_history:
            conn.send("\n".join(conversation_history).encode())
        else:
            conn.send(b"No previous messages.\n")

        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    print(f"Client {addr} disconnected.")
                    break

                message = f"Client {addr}: {data}"
                print(message)
                conversation_history.append(message)
                broadcast_message(message, sender_conn=conn)
            except ConnectionResetError:
                print(f"Connection lost with {addr}")
                break

    clients.remove((conn, addr))
    conn.close()

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started and listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            clients.append((conn, addr))
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"Active connections: {len(clients)}")


if __name__ == "__main__":
    host_ = '192.168.118.238'
    port_ = 12345
    start_server(host_, port_)
