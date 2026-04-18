from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os

OUTPUT_DIR = "outputs"

def generate_pdf(data, filename, include_answers=False, subject="General"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filepath = os.path.join(OUTPUT_DIR, filename)

    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>SSC Practice Paper</b>", styles["Title"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"<b>Subject:</b> {subject}", styles["Normal"]))
    story.append(Paragraph("<b>Time:</b> 60 min | <b>Marks:</b> 100", styles["Normal"]))
    story.append(Spacer(1, 10))

    for i, q in enumerate(data, 1):
        story.append(Paragraph(f"{i}. {q['question']}", styles["Normal"]))
        story.append(Paragraph(f"A. {q['options']['A']}", styles["Normal"]))
        story.append(Paragraph(f"B. {q['options']['B']}", styles["Normal"]))
        story.append(Paragraph(f"C. {q['options']['C']}", styles["Normal"]))
        story.append(Paragraph(f"D. {q['options']['D']}", styles["Normal"]))

        if include_answers:
            story.append(Paragraph(f"<b>Answer:</b> {q['answer']}", styles["Normal"]))

        story.append(Spacer(1, 10))

    doc.build(story)
    return filepath
