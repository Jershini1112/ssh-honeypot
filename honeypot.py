import socket
import threading
import datetime

LOG_FILE = "honeypot_log.txt"

def log_attempt(ip, username, password):
    timestamp = datetime.datetime.now()
    log = f"[{timestamp}] IP: {ip} | Username: {username} | Password: {password}\n"
    print(log)
    with open(LOG_FILE, "a") as f:
        f.write(log)

def handle_connection(conn, addr):
    ip = addr[0]
    try:
        conn.send(b"SSH-2.0-OpenSSH_8.9\r\n")
        data = conn.recv(1024).decode(errors="ignore")
        parts = data.strip().split(":")
        username = parts[0] if len(parts) > 0 else "unknown"
        password = parts[1] if len(parts) > 1 else "unknown"
        log_attempt(ip, username, password)
        conn.send(b"Permission denied\r\n")
    except:
        pass
    finally:
        conn.close()

def start_honeypot(port=2222):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Honeypot running on port {port}...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()

start_honeypot()