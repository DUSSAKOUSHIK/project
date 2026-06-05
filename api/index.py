from flask import Flask, request, jsonify
import json
import xml.etree.ElementTree as ET
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import base64

app = Flask(__name__)

@app.route('/api/employee', methods=['POST'])
def create_employee():
    try:
        data = request.json
        emp_id = data.get('id')
        name = data.get('name')
        department = data.get('department')
        salary = data.get('salary')
        
        if not all([emp_id, name, department, salary]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        employee = {
            "id": emp_id,
            "name": name,
            "department": department,
            "salary": salary
        }
        
        # Create JSON
        json_data = json.dumps(employee, indent=4)
        
        # Create XML
        root = ET.Element("employee")
        for key, value in employee.items():
            child = ET.SubElement(root, key)
            child.text = value
        
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Create PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer)
        styles = getSampleStyleSheet()
        
        elements = []
        elements.append(Paragraph("Employee Details Report", styles['Title']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"<b>Employee ID:</b> {emp_id}", styles['Normal']))
        elements.append(Paragraph(f"<b>Name:</b> {name}", styles['Normal']))
        elements.append(Paragraph(f"<b>Department:</b> {department}", styles['Normal']))
        elements.append(Paragraph(f"<b>Salary:</b> {salary}", styles['Normal']))
        
        doc.build(elements)
        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'employee': employee,
            'json': json_data,
            'xml': xml_str,
            'pdf': pdf_base64
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)
