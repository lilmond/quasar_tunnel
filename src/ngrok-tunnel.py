import threading
import socket

# Ngrok
LISTEN_TO_HOST = "0.0.0.0"
LISTEN_TO_PORT = 4444

# RAT server
ROUTE_TO_HOST = "127.0.0.1"
ROUTE_TO_PORT = 4445

BUFF_SIZE = 4096

class CLIENTS:
    connect_count = 0

def main():
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_server.bind((LISTEN_TO_HOST, LISTEN_TO_PORT))
    sock_server.listen()
    print(F"Listening to {LISTEN_TO_HOST}:{LISTEN_TO_PORT}...")

    while True:
        client = sock_server.accept()
        threading.Thread(target=client_handle, args=[client], daemon=False).start()

def client_handle(client):
    CLIENTS.connect_count += 1
    client_id = CLIENTS.connect_count
    client_sock, client_address = client
    client_host, client_port = client_address
    
    print(f"Client {client_id} ({client_host}:{client_port}): Connected. Creating route socket...")

    route_sock = create_route_socket()
    if not route_sock: client_sock.close(); return
    threading.Thread(target=route, args=[route_sock, client_sock], daemon=False).start()
    threading.Thread(target=route, args=[client_sock, route_sock], daemon=False).start()
    
    print(f"Client {client_id} ({client_host}:{client_port}): Routing...")

def create_route_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ROUTE_TO_HOST, ROUTE_TO_PORT))

        return sock
    except Exception:
        print("Error: Unable to create route socket")
        return

def route(route_from, route_to):
    try:
        while True:
            data = route_from.recv(BUFF_SIZE)
            if len(data) == 0: break
            route_to.send(data)
        
        route_from.close()
        route_to.close()
    except Exception:
        return

if __name__ == "__main__":
    main()
