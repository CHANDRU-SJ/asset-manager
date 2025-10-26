from io import BytesIO
from pathlib import Path
from typing import List, Union
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from PyPDF2 import PdfWriter


def generate_table_pdf(
    data_list: List[Union[dict, object]],
    columns: List[str],
    filepath: Path,
    title: str = "Data Report",
) -> str:
    """
    Generates a clean, tabular PDF report from a list of dicts or objects.
    Saves to `filepath` and returns the file path as string.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40,
    )

    # Title setup with style
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        alignment=1,  # center
        textColor=colors.HexColor("#0B5394"),
        spaceAfter=20,
    )
    title_para = Paragraph(title, title_style)
    spacer = Spacer(1, 15)
    
    # define a style for cell text
    cell_style = ParagraphStyle(
        name="CellStyle",
        fontName="Helvetica",
        fontSize=10,
        alignment=1,  # center; use 0=left, 2=right if needed
        leading=12,   # line height
    )

    # Prepare table data
    table_data = [columns]

    for item in data_list:
        row = []
        for col in columns:
            if isinstance(item, dict):
                value = item.get(col, "")
            else:
                value = getattr(item, col, "")
            row.append(Paragraph(str(value), cell_style))
        table_data.append(row)

    # Table with margins (not full width)
    page_width, _ = A4
    table_width = page_width * 0.90  # table takes 85% of page width
    col_width = table_width / len(columns)
    table = Table(table_data, colWidths=[col_width] * len(columns), hAlign="CENTER")

    # Table styling
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4B8BBE")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )

    # Build PDF
    elements = [title_para, spacer, table]
    doc.build(elements)

    # Save via PyPDF2
    buffer.seek(0)
    pdf_writer = PdfWriter()
    pdf_writer.append(buffer)

    with open(filepath, "wb") as f:
        pdf_writer.write(f)

    return str(filepath)
