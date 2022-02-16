import threading
import socket
import time

# your running server
SERVER_HOST = "135.82.217.36"
SERVER_PORT = 4445

# where data will be routed to
ROUTE_TO_HOST = "127.0.0.1"
ROUTE_TO_PORT = 4445

def marry(port):
    try:
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect((SERVER_HOST, port))
    except Exception:
        print(f"error: unable to connect to {SERVER_HOST}:{port}")
        return

    try:
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect((ROUTE_TO_HOST, ROUTE_TO_PORT))
    except Exception:
        print(f"error: unable to connect to {ROUTE_TO_HOST}:{ROUTE_TO_PORT}")
        return

    threading.Thread(target=packet_router, args=[sock1, sock2], daemon=True).start()
    threading.Thread(target=packet_router, args=[sock2, sock1], daemon=True).start()

def packet_router(src, dst):
    src_host, src_port = src.getpeername()
    dst_host, dst_port = dst.getpeername()

    print(f"notice: packet router started {src_host}:{src_port} -> {dst_host}:{dst_port}")

    try:
        while True:
            data = src.recv(4096)

            if len(data) == 0: break

            dst.send(data)
    except Exception:
        return

    finally:
        src.close()
        dst.close()
        print(f"notice: packet router ended {src_host}:{src_port} -> {dst_host}:{dst_port}")

def listener():
    while True:
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((SERVER_HOST, SERVER_PORT))
            print(f"notice: connected")
        except Exception:
            print(f"error: unable to connect to server")
            time.sleep(3)
            continue

        while True:
            data = server_sock.recv(1024)
            if len(data) == 0: break

            port = int(data.decode())
            threading.Thread(target=marry, args=[port], daemon=True).start()

def main():
    threading.Thread(target=listener, daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
