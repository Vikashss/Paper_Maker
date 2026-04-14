from fpdf import FPDF
import os

OUTPUT_DIR = "outputs"

def generate_pdf(data, filename, include_answers=False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for i, q in enumerate(data, 1):
        pdf.multi_cell(0, 10, f"{i}. [{q['subject']}] {q['question']}")

        for key, val in q['options'].items():
            pdf.cell(0, 10, f"   {key}. {val}", ln=True)

        if include_answers:
            pdf.cell(0, 10, f"Answer: {q['answer']}", ln=True)

        pdf.ln(5)

    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)

    return filepath
