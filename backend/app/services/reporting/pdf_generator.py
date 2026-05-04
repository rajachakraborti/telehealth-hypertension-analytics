from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
from typing import Dict, Any
import os


class PDFGenerator:
    def __init__(self):
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(self.buffer, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.elements = []

    def add_title(self, title: str) -> None:
        """Add a title to the PDF."""
        title_style = self.styles['Heading1']
        self.elements.append(Paragraph(title, title_style))
        self.elements.append(Spacer(1, 12))

    def add_section(self, section_title: str, content: str) -> None:
        """Add a section with title and content."""
        heading_style = self.styles['Heading2']
        body_style = self.styles['Normal']

        self.elements.append(Paragraph(section_title, heading_style))
        self.elements.append(Spacer(1, 6))
        self.elements.append(Paragraph(content, body_style))
        self.elements.append(Spacer(1, 12))

    def save_pdf(self, filename: str) -> str:
        """Save PDF to file and return the filepath."""
        self.doc.build(self.elements)
        with open(filename, 'wb') as f:
            f.write(self.buffer.getvalue())
        return filename

    def get_pdf_bytes(self) -> bytes:
        """Get PDF content as bytes."""
        self.doc.build(self.elements)
        return self.buffer.getvalue()


def generate_pdf_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a PDF report from provided data.

    Args:
        data: Dictionary containing report data with optional keys:
            - title: Report title
            - sections: List of {title, content} dictionaries

    Returns:
        Dictionary with report generation status and details
    """
    report = PDFGenerator()

    # Set title
    title = data.get('title', 'Telehealth Hypertension Analytics Report')
    report.add_title(title)

    # Add sections
    sections = data.get('sections', [])
    for section in sections:
        section_title = section.get('title', 'Section')
        content = section.get('content', '')
        report.add_section(section_title, content)

    # If no sections provided, add a default one
    if not sections:
        report.add_section(
            'Summary',
            'This report contains analytics data for telehealth hypertension management.'
        )

    # Save to uploads directory
    os.makedirs('uploads/reports', exist_ok=True)
    import uuid
    filename = f"uploads/reports/report_{uuid.uuid4().hex[:8]}.pdf"
    filepath = report.save_pdf(filename)

    return {
        "status": "success",
        "filepath": filepath,
        "title": title
    }


# Example usage
if __name__ == "__main__":
    data = {
        "title": "Telehealth Hypertension Predictive Analytics Report",
        "sections": [
            {
                "title": "Introduction",
                "content": "This report provides insights into the hypertension management through telehealth interventions."
            },
            {
                "title": "Findings",
                "content": "The analysis shows significant improvements in patient outcomes."
            }
        ]
    }
    result = generate_pdf_report(data)
    print(f"Report generated: {result}")
