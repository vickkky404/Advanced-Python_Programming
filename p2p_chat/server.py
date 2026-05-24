"""
P2P Chat App - Server
Manages all connected clients and broadcasts messages.
"""

import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

clients = {}   # socket -> username
lock = threading.Lock()


def broadcast(message: str, sender_socket=None):
    """Send a message to all connected clients except the sender."""
    with lock:
        for client_socket in list(clients):
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode('utf-8'))
                except Exception:
                    remove_client(client_socket)


def broadcast_all(message: str):
    """Send a message to ALL connected clients (e.g. join/leave notices)."""
    with lock:
        for client_socket in list(clients):
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception:
                remove_client(client_socket)


def remove_client(client_socket):
    """Remove a client from the registry (must be called with lock held)."""
    username = clients.pop(client_socket, None)
    try:
        client_socket.close()
    except Exception:
        pass
    return username


def handle_client(client_socket, address):
    """Dedicated thread for each connected client."""
    print(f"[+] New connection from {address}")

    # First message from client is always their username
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()
        if not username:
            client_socket.close()
            return
    except Exception:
        client_socket.close()
        return

    with lock:
        clients[client_socket] = username

    print(f"[+] {username} joined the chat.")
    broadcast_all(f"[SERVER] {username} has joined the chat! 👋")

    while True:
        try:
            message = client_socket.recv(2048).decode('utf-8')
            if not message:
                break
            print(f"[{username}]: {message}")
            broadcast(f"[{username}]: {message}", sender_socket=client_socket)
        except Exception:
            break

    # Client disconnected
    with lock:
        username = remove_client(client_socket)

    if username:
        print(f"[-] {username} left the chat.")
        broadcast_all(f"[SERVER] {username} has left the chat.")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    print(f"🚀 Server started on {HOST}:{PORT}")
    print("Waiting for clients...\n")

    try:
        while True:
            client_socket, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()