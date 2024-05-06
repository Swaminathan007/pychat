import socket
import threading


SERVER_HOST = '0.0.0.0' 
SERVER_PORT = 12345

def handle_client(client_socket, address):
    global msgs
    print(f"[NEW CONNECTION] {address} connected.")

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                print(f"[DISCONNECTED] {address} disconnected.")
                break
            print(f"[{address}] {message}")
            msgs.append(message)
            broadcast_message(message)
        except Exception as e:
            print(f"[EXCEPTION] {address} {e}")
            break

    client_socket.close()

def broadcast_message(message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode("utf-8"))
        except:
            clients.remove(client_socket)

clients = []
msgs = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f"[LISTENING] Server is listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, address = server_socket.accept()
    clients.append(client_socket)
    if len(msgs) > 0:
        for m in msgs:
            try:
                client_socket.send(m.encode("utf-8"))
            except:
                clients.remove(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
