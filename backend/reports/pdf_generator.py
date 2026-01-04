from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
from datetime import datetime
from typing import Dict

def generate_city_report(city_name: str, indicators: Dict, insights: Dict, recommendations: List[Dict]) -> BytesIO:
    """
    Generate professional PDF planning report
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#06b6d4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Title Page
    elements.append(Spacer(1, 2*inch))
    title = Paragraph(f"<b>UrbanPulse AI</b><br/>Urban Planning Intelligence Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    subtitle = Paragraph(f"<b>{city_name.title()}, Kenya</b>", styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.2*inch))
    
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal'])
    elements.append(date_text)
    
    elements.append(PageBreak())
    
    # Executive Summary
    elements.append(Paragraph("<b>Executive Summary</b>", heading_style))
    
    pop_density = indicators.get('population_density', {})
    land_use = indicators.get('land_use', {})
    service_access = indicators.get('service_accessibility', {})
    
    summary_text = f"""
    This report presents a comprehensive analysis of {city_name.title()}'s urban development patterns, 
    infrastructure adequacy, and planning recommendations. Key findings include:
    <br/><br/>
    • Total Population: <b>{pop_density.get('total_population', 0):,}</b> residents<br/>
    • Average Density: <b>{pop_density.get('avg_density', 0):.2f}</b> people/km²<br/>
    • Built-up Area: <b>{land_use.get('built_up_percentage', 0):.2f}%</b><br/>
    • Service Accessibility: <b>{service_access.get('accessibility_score', 0):.2f}/100</b><br/>
    <br/>
    The analysis identifies <b>{len(insights.get('issues', []))}</b> critical planning issues and proposes 
    <b>{len(recommendations)}</b> actionable recommendations for sustainable urban development.
    """
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Urban Indicators Section
    elements.append(Paragraph("<b>Urban Indicators Overview</b>", heading_style))
    
    # Population Density Table
    elements.append(Paragraph("<b>Population Density by Zone</b>", styles['Heading3']))
    density_data = [['Zone', 'Population', 'Area (km²)', 'Density (ppl/km²)']]
    
    for zone in pop_density.get('zones', [])[:5]:
        density_data.append([
            zone.get('name', ''),
            f"{zone.get('population', 0):,}",
            f"{zone.get('area_km2', 0):.2f}",
            f"{zone.get('density', 0):,}"
        ])
    
    density_table = Table(density_data, colWidths=[2*inch, 1.5*inch, 1.2*inch, 1.5*inch])
    density_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(density_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Service Accessibility
    elements.append(Paragraph("<b>Service Accessibility</b>", styles['Heading3']))
    service_data = [
        ['Metric', 'Value'],
        ['Accessibility Score', f"{service_access.get('accessibility_score', 0):.2f}/100"],
        ['Total Hospitals', str(service_access.get('total_hospitals', 0))],
        ['Hospital Capacity', f"{service_access.get('hospital_capacity', 0):,} beds"],
        ['Total Schools', str(service_access.get('total_schools', 0))],
        ['School Capacity', f"{service_access.get('school_capacity', 0):,} students"],
    ]
    
    service_table = Table(service_data, colWidths=[3*inch, 3*inch])
    service_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06b6d4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(service_table)
    elements.append(PageBreak())
    
    # AI Insights Section
    elements.append(Paragraph("<b>AI-Generated Planning Insights</b>", heading_style))
    
    for idx, issue in enumerate(insights.get('issues', []), 1):
        issue_title = Paragraph(f"<b>{idx}. {issue.get('title', '')}</b> [{issue.get('severity', '').upper()}]", styles['Heading3'])
        elements.append(issue_title)
        issue_desc = Paragraph(issue.get('description', ''), body_style)
        elements.append(issue_desc)
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(PageBreak())
    
    # Recommendations Section
    elements.append(Paragraph("<b>Planning Recommendations</b>", heading_style))
    
    for idx, rec in enumerate(recommendations, 1):
        rec_title = Paragraph(
            f"<b>{idx}. {rec.get('title', '')}</b> [Priority: {rec.get('priority', '')}]",
            styles['Heading3']
        )
        elements.append(rec_title)
        
        rec_desc = Paragraph(rec.get('description', ''), body_style)
        elements.append(rec_desc)
        
        # Specific Action
        if 'specific_action' in rec:
            action = rec['specific_action']
            action_text = "<b>Specific Action:</b><br/>"
            for key, value in action.items():
                if isinstance(value, list):
                    action_text += f"• {key.replace('_', ' ').title()}: {', '.join(str(v) for v in value)}<br/>"
                else:
                    action_text += f"• {key.replace('_', ' ').title()}: {value}<br/>"
            
            elements.append(Paragraph(action_text, body_style))
        
        # Expected Impact
        if 'expected_impact' in rec:
            impact = rec['expected_impact']
            impact_text = "<b>Expected Impact:</b><br/>"
            for key, value in impact.items():
                impact_text += f"• {key.replace('_', ' ').title()}: {value}<br/>"
            
            elements.append(Paragraph(impact_text, body_style))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
