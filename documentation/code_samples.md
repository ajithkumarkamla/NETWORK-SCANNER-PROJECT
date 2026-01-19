# Sample Code Snippets for Network Scanner

## 1. ARP Discovery Logic
```python
import scapy.all as scapy

def scan_network(ip_range):
    # Create ARP Request
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    
    # Send and Receive
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    devices = []
    for element in answered_list:
        devices.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return devices
```

## 2. Multi-threaded Port Scanning
```python
import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            return port
    return None

def run_scanner(ip, ports):
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(ip, p), ports)
        return [p for p in results if p]
```
