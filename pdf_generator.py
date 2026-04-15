from fpdf import FPDF
import os

OUTPUT_DIR = "outputs"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("NotoSans", "B", 14)
        self.cell(0, 10, "Objective Question Paper", 0, 1, "C")
        self.ln(5)

def generate_pdf(data, filename, include_answers=False):
    ensure_output_dir()

    pdf = PDF()
    pdf.add_page()

    # ✅ ADD UNICODE FONT
    pdf.add_font("NotoSans", "", "fonts/NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSans", "B", "fonts/NotoSans-Bold.ttf", uni=True)

    pdf.set_font("NotoSans", size=12)

    for i, q in enumerate(data, 1):
        pdf.multi_cell(0, 10, f"{i}. {q['question']}")

        for key, val in q['options'].items():
            pdf.cell(0, 10, f"{key}. {val}", ln=True)

        if include_answers:
            pdf.cell(0, 10, f"Answer: {q['answer']}", ln=True)

        pdf.ln(5)

    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)

    return filepath
