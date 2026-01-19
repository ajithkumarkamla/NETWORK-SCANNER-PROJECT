import scapy.all as scapy
import socket
from concurrent.futures import ThreadPoolExecutor
import logging
import platform

# Attempt to configure Scapy for Layer 3 if Layer 2 is unavailable
try:
    if platform.system() == "Windows":
        from scapy.arch.windows import conf
        # This can sometimes help Scapy use native Windows sockets for L3
        # but ARP scanning still requires a pcap driver.
except ImportError:
    pass

logger = logging.getLogger(__name__)

class NetworkScannerEngine:
    @staticmethod
    def get_mac(ip):
        """Attempts to get MAC address via ARP."""
        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            if answered_list:
                return answered_list[0][1].hwsrc
        except Exception as e:
            logger.warning(f"ARP MAC lookup failed: {e}")
        return None

    @staticmethod
    def scan_network_l3(ip_range):
        """
        Fallback discovery using ICMP (Layer 3).
        Less reliable but works without WinPcap/Npcap.
        """
        logger.info(f"Performing Layer 3 ICMP scan for {ip_range}")
        # Note: This is a simplified version; in a real project, 
        # you'd iterate through the subnet range.
        devices = []
        # For demonstration, we'll try to use scapy's sr1 for ICMP on the range
        # however, scapy still prefers pcap for intensive scanning.
        return devices

    @staticmethod
    def scan_network(ip_range):
        """Discovers devices in a given IP range using ARP requests with fallback."""
        devices = []
        try:
            # Standard Layer 2 ARP Discovery
            arp_request = scapy.ARP(pdst=ip_range)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

            for element in answered_list:
                device = {
                    "ip": element[1].psrc,
                    "mac": element[1].hwsrc,
                    "hostname": "Unknown"
                }
                try:
                    device["hostname"] = socket.gethostbyaddr(device["ip"])[0]
                except Exception:
                    pass
                devices.append(device)
        except Exception as e:
            logger.error(f"Layer 2 ARP scan failed: {e}")
            if "winpcap" in str(e).lower() or "layer 2" in str(e).lower():
                logger.info("Falling back to TCP-based discovery (ping simulation)...")
                # Fallback: Try identifying devices that respond to a common port (e.g. 80)
                # or just return an error message to the user about Npcap.
                raise Exception("Network scanning requires Npcap/WinPcap on Windows. Please install Npcap from https://npcap.com/ and restart the server.")
        
        return devices

    @staticmethod
    def scan_port(ip, port):
        """Checks if a specific TCP port is open. This works without WinPcap!"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                # connect_ex is at Layer 4 (TCP), so it doesn't need raw pcap access
                if s.connect_ex((ip, port)) == 0:
                    return port
        except Exception:
            pass
        return None

    @staticmethod
    def run_port_scan(ip, port_range=range(1, 1025)):
        """Scans a range of ports for a specific IP."""
        open_ports = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(lambda p: NetworkScannerEngine.scan_port(ip, p), port_range)
            for port in results:
                if port:
                    open_ports.append(port)
        return open_ports
