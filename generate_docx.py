import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_project_docx():
    doc = Document()
    
    # --- Title Page ---
    title = doc.add_heading('Project Report: Network Scanner Tool', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph()
    run = p.add_run('\nReal-time Network Monitoring and Security Auditing System\n')
    run.bold = True
    run.font.size = Pt(14)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph('\n\nFinal Year Engineering Project')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()
    
    # --- 1. Project Overview ---
    doc.add_heading('1. Project Overview', level=1)
    doc.add_paragraph(
        "The Network Scanner Tool is a sophisticated security application designed for local area network (LAN) auditing. "
        "Its primary objective is to provide network administrators with a real-time view of active devices, "
        "open services (ports), and potential security vulnerabilities within a subnet."
    )
    
    doc.add_heading('1.1 Objectives', level=2)
    objectives = [
        'Device Discovery: Automate the identification of all active hosts in a given IP range.',
        'Port Auditing: Identify open ports and the services running on them.',
        'Real-time Monitoring: Provide a dynamic dashboard that updates as devices join or leave the network.',
        'Reporting: Generate professional-grade audit reports for compliance and documentation.'
    ]
    for obj in objectives:
        doc.add_paragraph(obj, style='List Bullet')
        
    # --- 2. Features ---
    doc.add_heading('2. Features', level=1)
    features = [
        'LAN / IP Range Scanning: Supports CIDR notation (e.g., 192.168.1.0/24).',
        'Active Device Detection: IP Address, MAC Address, Hostname, and Vendor Detection.',
        'Port Scanning: Multi-threaded scanning of TCP ports.',
        'Interactive Dashboard: Premium Glassmorphism web UI.',
        'Mobile QR Scan: Dynamic QR code for mobile webscan access.',
        'Professional Reporting: Automated PDF generation.'
    ]
    for feat in features:
        doc.add_paragraph(feat, style='List Bullet')
        
    # --- 3. Technology Stack ---
    doc.add_heading('3. Technology Stack', level=1)
    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Component'
    hdr_cells[1].text = 'Technology'
    hdr_cells[2].text = 'Rationale'
    
    tech_data = [
        ('Backend', 'Python', 'Robust libraries for networking.'),
        ('Networking', 'Scapy, Socket', 'Low-level packet manipulation & TCP.'),
        ('Web Framework', 'Django', 'Secure & scalable management system.'),
        ('Database', 'SQLite', 'Efficient storage of scan history.'),
        ('Reporting', 'ReportLab', 'Professional PDF generation.')
    ]
    for comp, tech, rat in tech_data:
        row_cells = table.add_row().cells
        row_cells[0].text = comp
        row_cells[1].text = tech
        row_cells[2].text = rat
    table.style = 'Table Grid'
    
    # --- 4. System Architecture ---
    doc.add_heading('4. System Architecture', level=1)
    doc.add_paragraph("The system follows a modular architecture where the scanning engine is decoupled from the user interface.")
    
    img_path = 'documentation/flowchart_viva.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(5))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph('Figure 1: System Architecture and Data Flow', style='Caption').alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # --- 5. Viva Preparation ---
    doc.add_page_break()
    doc.add_heading('5. Viva Voce Preparation (Q&A)', level=1)
    
    qa_data = [
        ("Q1: Why use Scapy instead of the standard socket library for discovery?", 
         "Answer: Scapy allows manipulation of raw packets at Layer 2 (ARP), which is more reliable than ICMP (Ping) as it bypasses many local firewalls."),
        ("Q2: How is port scanning performance optimized?", 
         "Answer: We use multi-threading with ThreadPoolExecutor to scan multiple ports in parallel, significantly reducing scan time."),
        ("Q3: What is the benefit of the mobile QR scan feature?", 
         "Answer: It provides seamless 'WebScan' access, allowing administrators to monitor the network from any mobile device without manual configuration.")
    ]
    for q, a in qa_data:
        p = doc.add_paragraph()
        p.add_run(q).bold = True
        doc.add_paragraph(a)
        
    # --- 6. Implementation Samples ---
    doc.add_heading('6. Core Implementation Snippets', level=1)
    doc.add_heading('ARP Discovery Script', level=2)
    code1 = (
        "def scan_network(ip_range):\n"
        "    arp_request = scapy.ARP(pdst=ip_range)\n"
        "    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')\n"
        "    answered_list = scapy.srp(broadcast / arp_request, timeout=1, verbose=False)[0]\n"
        "    return [{'ip': e[1].psrc, 'mac': e[1].hwsrc} for e in answered_list]"
    )
    p = doc.add_paragraph(code1, style='No Spacing')
    p.runs[0].font.name = 'Courier New'
    
    # --- Save ---
    output_path = 'documentation/Project_Report_Network_Scanner.docx'
    doc.save(output_path)
    print(f"Word document generated at: {output_path}")

if __name__ == "__main__":
    generate_project_docx()
