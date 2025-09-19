# 🛡️ Port Scanner
A real-time multithreaded port scanner built in Python. This tool scans a target IP or domain for open ports and optionally grabs service banners to identify running services. It also logs TTL values to estimate the operating system and integrates Nmap and traceroute for deeper analysis.

**🚀 Features**
- 🔍 Scans ports 1–1024
- ⚡ Fast multithreaded scanning
- 🧠 Banner grabbing (optional service info)
- 📝 Logs results with timestamps
- 📁 Auto-creates scan_logs/ folder for output
- 🌐 Nmap service detection (if installed)
- 🛰️ Traceroute with geolocation and ISP info
- 🧠 OS guessing based on TTL values

**🛠️ How to Run**

```python scanner.py```


When prompted, enter a target IP or domain (e.g. scanme.nmap.org or 192.168.1.1). You can also paste full URLs like https://example.com.

**📁 Output**

Results are saved in the scan_logs/ folder with a timestamped filename:
```scan_logs/scanme.nmap.org_2025-09-20_00-09-00.txt```


Each line shows open ports and any banner info:
```
Port 22: OPEN → SSH-2.0-OpenSSH_8.2 [TTL: 64, OS Guess: Linux/Unix]
Port 80: OPEN → HTTP/1.1 200 OK [TTL: 128, OS Guess: Windows]
```

Includes Nmap service detection and traceroute with country, ISP, and organization info.

**📈 Future Improvements**
- Export results to CSV
- Scan multiple targets from a file
- Add GUI with Tkinter
- Add command-line flags with argparse
- CMS detection (WordPress, Joomla, etc.)

**📚 License**
This project is for educational and ethical hacking purposes only. Use responsibly.

Let me know if you want help writing a GitHub profile tagline, adding a license file (MIT, GPL, etc.), or creating a requirements.txt for easy setup. You're building a professional-grade tool!

