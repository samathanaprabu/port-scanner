import socket
import threading
from datetime import datetime
import os
from urllib.parse import urlparse
import subprocess
import requests
import re

# Ensure log folder exists
os.makedirs("scan_logs", exist_ok=True)

# Validate domain
def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

# Input and strip scheme if URL is provided
raw_input = input("Enter target IP or domain (URL allowed): ")
parsed = urlparse(raw_input)
target_input = parsed.hostname if parsed.hostname else raw_input

# Check domain validity
if not is_valid_domain(target_input):
    print("Invalid or unreachable domain.")
    exit()

# Resolve domain to IP
target_ip = socket.gethostbyname(target_input)

# Scan settings
start_port = 1
end_port = 1024
open_ports = []
start_time = datetime.now()
timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"scan_logs/{target_input}_{timestamp}.txt"

# Port scanning function with banner and TTL
def scan_port(port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((target_ip, port))
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "No banner"
        try:
            ttl = s.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
        except:
            ttl = "Unknown"
        if ttl == 128:
            os_guess = "Windows"
        elif ttl == 64:
            os_guess = "Linux/Unix"
        elif ttl == 255:
            os_guess = "Cisco/Network device"
        else:
            os_guess = "Unknown"
        print(f"Port {port}: OPEN → {banner} [TTL: {ttl}, OS Guess: {os_guess}]")
        open_ports.append((port, banner, ttl, os_guess))
        s.close()
    except:
        pass

# Start scanning
print(f"[{start_time.strftime('%H:%M:%S')}] Scanning {target_input} ({target_ip})...")

threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Run Nmap for service detection
print("Running Nmap service detection...")
try:
    nmap_output = subprocess.check_output(["nmap", "-sV", target_input], text=True)
except Exception as e:
    nmap_output = f"Nmap scan failed: {e}"

# Run Traceroute and enrich with IP info
print("Running traceroute and geolocation...")
try:
    traceroute_raw = subprocess.check_output(["tracert", target_input], text=True)
    hop_ips = re.findall(r"\d+\.\d+\.\d+\.\d+", traceroute_raw)
    traceroute_info = []
    for ip in hop_ips:
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
            traceroute_info.append({
                "ip": ip,
                "country": geo.get("country", "Unknown"),
                "isp": geo.get("isp", "Unknown"),
                "org": geo.get("org", "Unknown")
            })
        except:
            traceroute_info.append({
                "ip": ip,
                "country": "Unknown",
                "isp": "Unknown",
                "org": "Unknown"
            })
except Exception as e:
    traceroute_info = [f"Traceroute failed: {e}"]

# Finish scan
end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

# Save results
with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"Scan Target: {target_input}\n")
    f.write(f"Resolved IP: {target_ip}\n")
    f.write(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Duration: {duration:.2f} seconds\n\n")
    for port, banner, ttl, os_guess in open_ports:
        f.write(f"Port {port}: OPEN → {banner} [TTL: {ttl}, OS Guess: {os_guess}]\n")
    f.write("\n--- Nmap Service Detection ---\n")
    f.write(nmap_output)
    f.write("\n--- Traceroute & IP Info ---\n")
    for hop in traceroute_info:
        if isinstance(hop, dict):
            f.write(f"{hop['ip']} → {hop['country']} | ISP: {hop['isp']} | Org: {hop['org']}\n")
        else:
            f.write(f"{hop}\n")

print(f"Scan completed in {duration:.2f} seconds.")
print(f"Results saved to {log_file}")
