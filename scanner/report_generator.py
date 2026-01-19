from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import datetime
import io

class ReportGenerator:
    @staticmethod
    def generate_pdf_report(devices):
        """
        Generates a PDF report of the discovered devices.
        Returns a byte buffer.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        header_style = styles['Heading2']
        body_style = styles['BodyText']
        
        # Title
        elements.append(Paragraph("Network Audit Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Metadata
        elements.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
        elements.append(Paragraph(f"Total Devices Discovered: {len(devices)}", body_style))
        elements.append(Spacer(1, 20))
        
        # Table Data
        data = [['IP Address', 'MAC Address', 'Hostname', 'Open Ports']]
        for device in devices:
            ports = ", ".join(map(str, device.get('open_ports', []))) if device.get('open_ports') else "None"
            data.append([
                device.get('ip', 'N/A'),
                device.get('mac', 'N/A'),
                device.get('hostname', 'Unknown'),
                ports
            ])
            
        # Create Table
        table = Table(data, colWidths=[100, 130, 150, 100])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
