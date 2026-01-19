from django.contrib import admin
from .models import NetworkDevice, ScanResult

@admin.register(NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'hostname', 'mac_address', 'vendor', 'is_active', 'last_seen')
    list_filter = ('is_active', 'vendor')
    search_fields = ('ip_address', 'hostname', 'mac_address')
    ordering = ('-last_seen',)

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('device', 'scan_time', 'status')
    list_filter = ('status',)
    search_fields = ('device__ip_address',)
    ordering = ('-scan_time',)
