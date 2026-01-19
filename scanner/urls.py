from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/start/', views.start_scan, name='start_scan'),
    path('devices/', views.get_devices, name='get_devices'),
    path('history/<int:device_id>/', views.get_scan_history, name='get_scan_history'),
    path('report/download/', views.download_report, name='download_report'),
    path('qr/', views.generate_qr_code, name='generate_qr_code'),
]
