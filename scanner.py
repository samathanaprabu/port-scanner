import socket
import threading
from datetime import datetime
import os

# Ensure log folder exists
os.makedirs("scan_logs", exist_ok=True)

target = input("Enter target IP or domain: ")
start_port = 1
end_port = 1024
open_ports = []
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"scan_logs/{target}_{timestamp}.txt"

def scan_port(port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((target, port))
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "No banner"
        print(f"Port {port}: OPEN → {banner}")
        open_ports.append((port, banner))
        s.close()
    except:
        pass

print(f"[{datetime.now().strftime('%H:%M:%S')}] Scanning {target}...")

threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

with open(log_file, "w") as f:
    for port, banner in open_ports:
        f.write(f"Port {port}: OPEN → {banner}\n")

print(f"Results saved to {log_file}")
