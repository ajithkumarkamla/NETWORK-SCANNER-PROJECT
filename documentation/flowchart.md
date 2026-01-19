# Project Flowcharts

![Project Architecture Flowchart](./flowchart_viva.png)

This document contains visual flowcharts representing the logic and architecture of the Network Scanner Tool.

## 1. Overall System Architecture
This flowchart shows how the User, Django Backend, and Network Scanner Engine interact.

```mermaid
graph TD
    User((User/Admin)) -->|Access Dashboard| WebUI[Django Web Dashboard]
    WebUI -->|Auto-Scan / Manual Scan| API[Django REST API]
    API -->|Trigger Scan| Engine[Scanner Engine]
    
    subgraph "Backend Engine"
        Engine -->|ARP Request| L2[Layer 2 Discovery]
        Engine -->|TCP Connect| L4[Port Auditing]
    end
    
    L2 -->|Found Devices| Parser[Result Parser]
    L4 -->|Open Ports| Parser
    
    Parser -->|Save Data| DB[(SQLite Database)]
    DB -->|Fetch Results| API
    API -->|JSON Data| WebUI
    WebUI -->|Live Update| User
```

## 2. Scan Logic Flow (Step-by-Step)
This flowchart describes the internal logic of a single network scan.

```mermaid
flowchart TD
    Start([Start Scan]) --> Init[Mark all existing devices as Inactive]
    Init --> Discovery{ARP Discovery}
    
    Discovery -->|Device Found| GetMAC[Identify IP & MAC]
    GetMAC --> Hostname[Resolve Hostname]
    Hostname --> PortScan{Common Port Scan}
    
    PortScan --> Save[Save Results to Database]
    Save --> Active[Mark Device as Active]
    
    Active --> More{More Devices?}
    More -->|Yes| GetMAC
    More -->|No| Finish([Scan Complete])
    
    Discovery -->|No Devices| Finish
```

## 3. Mobile QR Access Flow
```mermaid
sequenceDiagram
    participant Laptop as Laptop (Server)
    participant Phone as Mobile Phone
    participant Router as WiFi Router
    
    Laptop->>Router: Bound to 0.0.0.0:8000
    Laptop->>Laptop: Generate QR with LAN IP (192.168.x.x)
    Phone->>Laptop: Scan QR Code
    Phone->>Laptop: Request Dashboard via LAN IP
    Laptop->>Phone: Serve Responsive Glassmorphism UI
```
