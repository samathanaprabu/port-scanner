# Port Scanner

A real-time multithreaded port scanner built in Python. This tool scans a target IP or domain for open ports and optionally grabs service banners to identify running services.

**🚀 Features**
- 🔍 Scans ports 1–1024
- ⚡ Fast multithreaded scanning
- 🧠 Banner grabbing (optional service info)
- 📝 Logs results with timestamps
- 📁 Auto-creates scan_logs/ folder for output

**🛠️ How to Run**

```python scanner.py```


When prompted, enter a target IP or domain (e.g. scanme.nmap.org or 192.168.1.1).

**📁 Output**

Results are saved in the scan_logs/ folder with a timestamped filename:

```scan_logs/scanme.nmap.org_2025-09-20_00-09-00.txt```


Each line shows open ports and any banner info:
```
Port 22: OPEN → SSH-2.0-OpenSSH_8.2
Port 80: OPEN → HTTP/1.1 200 OK
```


**📈 Future Improvements**
- Export results to CSV
- Scan multiple targets from a file
- Add GUI with Tkinter
- Add command-line flags with argparse

**📚 License**
This project is for educational and ethical hacking purposes only. Use responsibly.

Let me know if you'd like help writing a short description for your GitHub profile or adding a license file!


