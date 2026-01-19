from django.db import models

class NetworkDevice(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    vendor = models.CharField(max_length=255, blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ip_address} ({self.hostname or 'Unknown'})"

class ScanResult(models.Model):
    device = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE, related_name='scans')
    scan_time = models.DateTimeField(auto_now_add=True)
    open_ports = models.JSONField(default=list)  # List of integers
    os_info = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default="Completed")

    def __str__(self):
        return f"Scan for {self.device.ip_address} at {self.scan_time}"
