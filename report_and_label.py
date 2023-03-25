"""
Create PDF reports and labels for the buffers made.
Style accordingly and include as much information as possible.
Make it useful to enable a shift from Paperwork to full Digital

"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

##---------Basic Testing of PDF generation---------
def generate_pdf_report(buffer_name, chemical_weights, nameofbuffer_processor, batch_number):
    # Prepare the data for the table
    header = ["Chemical Name", "Adjusted Weight (g)"]
    table_data = [header]
    for chem_name, adjusted_weight in chemical_weights.items():
        table_data.append([chem_name, adjusted_weight])

    # Create a PDF document
    pdf_filename = f"data/files/{buffer_name}_Batch_{batch_number}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Create a Table object
    table = Table(table_data)

    # Apply a TableStyle
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the nameofbuffer_processor and batch_number to the PDF
    styles = getSampleStyleSheet()
    buffer_info = Paragraph(f"Buffer Name: <strong>{buffer_name}</strong><br/>"
                            f"Batch Number: <strong>{batch_number}</strong><br/>"
                            f"Name of Buffer Processor: <strong>{nameofbuffer_processor}</strong>",
                            styles['Normal'])

    # Add the table, buffer_info, and Spacer to the PDF document and build it
    elements = [buffer_info, Spacer(1, 24), table]
    doc.build(elements)
    print(f"PDF report saved as {pdf_filename}")

def create_lable(self):

    #Implemt buffer lables to be added to placed on the bottle
    pass