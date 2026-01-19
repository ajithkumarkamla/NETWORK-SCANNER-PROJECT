# PPT Outline & Viva Prep: Network Scanner Tool

## 1. PPT Slide Outline (10-12 Slides)

| Slide # | Title | Key Content Points |
| :--- | :--- | :--- |
| 1 | **Title Slide** | Project Name, Your Name, Supervisor, College Logo. |
| 2 | **Introduction** | Background of network security, problem statement. |
| 3 | **Objectives** | Real-time discovery, port auditing, reporting. |
| 4 | **Proposed System** | System overview, automated discovery feature. |
| 5 | **System Architecture** | Include the Block/Flow diagram. |
| 6 | **Modules** | Scanner, Port Scanner, Logger, Dashboard. |
| 7 | **Tech Stack** | Python, Django, Scapy, SQLite. |
| 8 | **Core Logic** | ARP Scanning and TCP Port Scanning. |
| 9 | **Key Features** | PDF reports, Glassmorphism UI, Mobile QR Scan. |
| 10 | **Screenshots/Demo** | Visual evidence of the tool in action. |
| 11 | **Conclusion** | Final summary and future enhancements. |
| 12 | **Q&A** | Thank you slide. |

---

## 2. Viva Voce Questions & Answers

### Q1: Why use Scapy instead of the standard socket library for discovery?
**Answer:** `Scapy` allows us to manipulate raw packets at Layer 2 (Data Link Layer). This is essential for **ARP Scanning**, which reliably finds devices even if they block ICMP (Ping) requests with a firewall.

### Q2: How does the "WebScan" QR feature work?
**Answer:** The server generates a QR code containing the server's LAN IP address. When a mobile device on the same Wi-Fi scans this, it opens the responsive dashboard directly in the mobile browser.

### Q3: How is performance maintained during port scanning?
**Answer:** We use **Multi-threading** with `ThreadPoolExecutor`. This allows the tool to check multiple ports simultaneously instead of waiting for each one one-by-one.

### Q4: Why is Django used for the backend?
**Answer:** Django provides a secure, structured framework for building the API and management dashboard. It easily handles database models, forms, and report generation via libraries like ReportLab.

---

## 3. Practical Demo Tips
- **Live Scan:** Connect your phone to the same Wi-Fi as your laptop. Run a scan and show your phone appearing in the dashboard list.
- **Port Detection:** Show how the scanner detects specific open ports like 80 (HTTP) or 443 (HTTPS).
- **PDF Report:** Demonstrate the one-click PDF generation and show the professional report layout.
