import os
import json
import xml.etree.ElementTree as ET
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
JSON_FILE = os.path.join(DATA_DIR, "employee.json")
XML_FILE = os.path.join(DATA_DIR, "employee.xml")
PDF_FILE = os.path.join(DATA_DIR, "employee.pdf")
emp_id = input("Enter Employee ID: ")
name = input("Enter Employee Name: ")
department = input("Enter Department: ")
salary = input("Enter Salary: ")
employee = {
    "id": emp_id,
    "name": name,
    "department": department,
    "salary": salary
}
with open(JSON_FILE, "w") as file:
    json.dump(employee, file, indent=4)

print("JSON file created successfully.")
root = ET.Element("employee")

for key, value in employee.items():
    child = ET.SubElement(root, key)
    child.text = value

tree = ET.ElementTree(root)
tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

print("XML file created successfully.")
doc = SimpleDocTemplate(PDF_FILE)
styles = getSampleStyleSheet()

elements = []

elements.append(Paragraph("Employee Details Report", styles['Title']))
elements.append(Spacer(1, 20))

elements.append(Paragraph(f"<b>Employee ID:</b> {emp_id}", styles['Normal']))
elements.append(Paragraph(f"<b>Name:</b> {name}", styles['Normal']))
elements.append(Paragraph(f"<b>Department:</b> {department}", styles['Normal']))
elements.append(Paragraph(f"<b>Salary:</b> {salary}", styles['Normal']))

doc.build(elements)

print("PDF file created successfully.")
print("\nEmployee Details")
print("--------------------------")
print("ID        :", emp_id)
print("Name      :", name)
print("Department:", department)
print("Salary    :", salary)
try:
    os.startfile(PDF_FILE)  # Windows
except Exception as e:
    print("Could not open PDF automatically.")
    print("Open manually from:", PDF_FILE)

print("\nFiles created in:")
print(os.path.abspath(DATA_DIR))