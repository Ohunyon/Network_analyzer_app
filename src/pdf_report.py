import os
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12
        )
        self.body_style = self.styles['Normal']

    def create_pie_chart(self, malicious, benign):
        plt.figure(figsize=(6, 4))
        labels = ['Malicious', 'Benign']
        sizes = [malicious, benign]
        colors = ['#ff9999', '#66b3ff']
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Traffic Distribution')
        
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)
        plt.close()
        
        return img_data

    def create_bar_chart(self, source_data):
        plt.figure(figsize=(8, 4))
        sources = list(source_data.keys())
        counts = list(source_data.values())
        
        plt.bar(sources, counts, color='#66b3ff')
        plt.title('Top Malicious Sources')
        plt.xlabel('Source IP')
        plt.ylabel('Number of Packets')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)
        plt.close()
        
        return img_data

    def generate_pdf(self, report_data, output_path):
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Title
        title = Paragraph("Network Traffic Analysis Report", self.title_style)
        story.append(title)
        
        # Generated at
        story.append(Paragraph(
            f"Generated on: {report_data['generated_at']}",
            self.body_style
        ))
        story.append(Spacer(1, 12))
        
        # Period
        period_text = f"Period: {report_data['period']['start']} to {report_data['period']['end']}"
        story.append(Paragraph(period_text, self.body_style))
        story.append(Spacer(1, 20))
        
        # Summary Statistics
        story.append(Paragraph("Summary Statistics", self.heading_style))
        summary_data = [
            ["Metric", "Value"],
            ["Total Packets", str(report_data['summary']['total_packets'])],
            ["Malicious Packets", str(report_data['summary']['malicious_packets'])],
            ["Benign Packets", str(report_data['summary']['benign_packets'])],
            ["Malicious Percentage", f"{report_data['summary']['malicious_percentage']:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 100])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Traffic Distribution Pie Chart
        story.append(Paragraph("Traffic Distribution", self.heading_style))
        pie_data = self.create_pie_chart(
            report_data['summary']['malicious_packets'],
            report_data['summary']['benign_packets']
        )
        story.append(Image(pie_data, width=400, height=300))
        story.append(Spacer(1, 20))
        
        # Top Malicious Sources Bar Chart
        story.append(Paragraph("Top Malicious Sources", self.heading_style))
        bar_data = self.create_bar_chart(report_data['top_malicious_sources'])
        story.append(Image(bar_data, width=500, height=300))
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("Recommendations", self.heading_style))
        recommendations = [
            "Monitor the identified malicious sources closely",
            "Consider implementing additional security measures for frequently targeted destinations",
            "Review and update firewall rules based on the traffic patterns",
            "Investigate any unusual spikes in malicious traffic"
        ]
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.body_style))
            story.append(Spacer(1, 6))
        
        # Build the PDF
        doc.build(story)
        return output_path
