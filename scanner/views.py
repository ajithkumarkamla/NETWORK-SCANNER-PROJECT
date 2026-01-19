from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from .scanner_engine import NetworkScannerEngine
from .models import NetworkDevice, ScanResult
from .report_generator import ReportGenerator
import json
import logging
import qrcode
import socket
from io import BytesIO

logger = logging.getLogger(__name__)

def index(request):
    """Main dashboard view."""
    return render(request, 'index.html')

@csrf_exempt
def start_scan(request):
    """
    Triggers a network scan for a given IP range.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip_range = data.get('ip_range', '192.168.1.0/24')
            
            # Reset activity status for all devices in this range (or all for simplicity)
            NetworkDevice.objects.update(is_active=False)
            
            # 1. Discover devices
            discovered_devices = NetworkScannerEngine.scan_network(ip_range)
            
            # 2. Update/Create devices in DB and perform port scans
            results = []
            for item in discovered_devices:
                device, created = NetworkDevice.objects.update_or_create(
                    ip_address=item['ip'],
                    defaults={
                        'mac_address': item['mac'],
                        'hostname': item['hostname'],
                        'is_active': True # Mark as found now
                    }
                )
                
                # ... (rest of the scan logic)
                common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
                open_ports = NetworkScannerEngine.run_port_scan(device.ip_address, common_ports)
                
                ScanResult.objects.create(
                    device=device,
                    open_ports=open_ports,
                    status="Completed"
                )
                
                results.append({
                    "id": device.id,
                    "ip": device.ip_address,
                    "mac": device.mac_address,
                    "hostname": device.hostname,
                    "is_active": True,
                    "open_ports": open_ports
                })
                
            return JsonResponse({"status": "success", "devices": results})
        except Exception as e:
            logger.error(f"Scan error: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def get_devices(request):
    """Returns only active (currently found) devices."""
    devices = NetworkDevice.objects.filter(is_active=True).order_by('-last_seen')
    data = []
    for d in devices:
        latest_scan = d.scans.last()
        data.append({
            "id": d.id,
            "ip": d.ip_address,
            "mac": d.mac_address,
            "hostname": d.hostname,
            "is_active": d.is_active,
            "last_seen": localtime(d.last_seen).strftime("%Y-%m-%d %I:%M:%S %p"),
            "open_ports": latest_scan.open_ports if latest_scan else []
        })
    return JsonResponse({"devices": data})

def get_scan_history(request, device_id):
    """Returns the scan history for a specific device."""
    scans = ScanResult.objects.filter(device_id=device_id).order_by('-scan_time')
    data = [{
        "time": localtime(s.scan_time).strftime("%Y-%m-%d %I:%M:%S %p"),
        "ports": s.open_ports,
        "status": s.status
    } for s in scans]
    return JsonResponse({"history": data})

def download_report(request):
    """Generates and returns a PDF report of all registered devices."""
    devices = NetworkDevice.objects.all()
    device_data = []
    for d in devices:
        latest_scan = d.scans.last()
        device_data.append({
            "ip": d.ip_address,
            "mac": d.mac_address,
            "hostname": d.hostname,
            "open_ports": latest_scan.open_ports if latest_scan else []
        })
    
    pdf_buffer = ReportGenerator.generate_pdf_report(device_data)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="network_report.pdf"'
    return response

def generate_qr_code(request):
    """Generates a QR code pointing to the server's LAN IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    
    server_url = f"http://{IP}:8000"
    
    # Very clear console instructions for the user
    print("\n" + "="*50)
    print("📱 MOBILE ACCESS READY")
    print(f"1. On your Phone, open: {server_url}")
    print(f"2. Or Scan the QR code shown on the dashboard")
    print("-"*50)
    print("⚠️ DO NOT type 'http://0.0.0.0:8000' in your browser.")
    print("   '0.0.0.0' is for the server to listen, not for you to visit.")
    print("="*50 + "\n")
    
    img = qrcode.make(server_url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
