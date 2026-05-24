# Chat client
# p2p chat app - Client..



import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5555

stop_event = threading.Event()

def receive_messages(client_socket):
    while not stop_event.is_set():
        try:
            message = client_socket.recv(2048).decode('utf-8')
            if not message:
                print("\n[!] Disconnected from server.")
                stop_event.set()
                break

            print(f"\r{message}\nYou: ", end="", flush=True)
        except Exception:
            if not stop_event.is_set():
                print("\n[!] Connection lost.")
                stop_event.set()
            break

def send_messages(client_socket):
    """
    Main thread: reads user input and sends it to the server.
    Type 'quit' or 'exit' to disconnect.
    """
    while not stop_event.is_set():
        try:
            message = input("You: ").strip()
            if not message:
                continue
            if message.lower() in ('quit', 'exit'):
                print("[*] Leaving chat...")
                stop_event.set()
                break
            client_socket.sendall(message.encode('utf-8'))
        except (EOFError, KeyboardInterrupt):
            print("\n[*] Leaving chat...")
            stop_event.set()
            break


def start_client():
    username = input("Enter your username: ").strip()
    if not username:
        print("[!] Username cannot be empty.")
        sys.exit(1)
 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[!] Could not connect to server at {HOST}:{PORT}")
        print("    Make sure server.py is running first.")
        sys.exit(1)
 
    print(f"\n✅ Connected to chat server as '{username}'")
    print("Type your message and press Enter. Type 'quit' to exit.\n")
 
    client_socket.sendall(username.encode('utf-8'))
 
    recv_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )
    recv_thread.start()
 

    send_messages(client_socket)
 

    client_socket.close()
    print("[*] Disconnected.")


if __name__ == "__main__":
    start_client()