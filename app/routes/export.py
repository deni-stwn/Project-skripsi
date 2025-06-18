from flask import Blueprint, jsonify, request, make_response, send_file
import csv
import io
import json
from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

export_bp = Blueprint('export', __name__)

@export_bp.route('/csv', methods=['POST'])
def export_csv():
    try:
        # Get results data from request
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'No data to export'}), 400
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['File 1', 'File 2', 'Similarity (%)', 'Risk Level', 'Export Date'])
        
        # Write data rows
        export_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for result in results:
            similarity = float(result.get('similarity', 0))
            risk_level = get_risk_level(similarity)
            writer.writerow([
                result.get('file_1', ''),
                result.get('file_2', ''),
                f"{similarity:.2f}",
                risk_level,
                export_date
            ])
        
        # Create response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=plagiarism_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@export_bp.route('/pdf', methods=['POST'])
def export_pdf():
    try:
        # Get results data from request
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'No data to export'}), 400
        
        # Create PDF content
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Title
        title = Paragraph("CodeScan Plagiarism Detection Report", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report info
        info_style = styles['Normal']
        export_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info = Paragraph(f"Generated on: {export_date}<br/>Total Comparisons: {len(results)}", info_style)
        story.append(info)
        story.append(Spacer(1, 20))
        
        # Summary statistics
        high_risk = len([r for r in results if float(r.get('similarity', 0)) >= 75])
        medium_risk = len([r for r in results if 50 <= float(r.get('similarity', 0)) < 75])
        low_risk = len([r for r in results if float(r.get('similarity', 0)) < 50])
        
        summary_data = [
            ['Risk Level', 'Count', 'Percentage'],
            ['High Risk (≥75%)', str(high_risk), f"{(high_risk/len(results)*100):.1f}%"],
            ['Medium Risk (50-74%)', str(medium_risk), f"{(medium_risk/len(results)*100):.1f}%"],
            ['Low Risk (<50%)', str(low_risk), f"{(low_risk/len(results)*100):.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Summary", styles['Heading2']))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detailed results table
        story.append(Paragraph("Detailed Results", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        # Prepare table data
        table_data = [['File 1', 'File 2', 'Similarity (%)', 'Risk Level']]
        
        for result in results:
            similarity = float(result.get('similarity', 0))
            risk_level = get_risk_level(similarity)
            table_data.append([
                result.get('file_1', '')[:30] + ('...' if len(result.get('file_1', '')) > 30 else ''),
                result.get('file_2', '')[:30] + ('...' if len(result.get('file_2', '')) > 30 else ''),
                f"{similarity:.2f}%",
                risk_level
            ])
        
        # Create table
        table = Table(table_data, colWidths=[2*inch, 2*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # Add color coding for risk levels
        for i, result in enumerate(results, 1):
            similarity = float(result.get('similarity', 0))
            if similarity >= 75:
                table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lightcoral)]))
            elif similarity >= 50:
                table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lightyellow)]))
            else:
                table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lightgreen)]))
        
        story.append(table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Create response
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=plagiarism_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_risk_level(similarity):
    """Get risk level based on similarity percentage"""
    if similarity >= 75:
        return "High Risk"
    elif similarity >= 50:
        return "Medium Risk"
    else:
        return "Low Risk"