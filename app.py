import streamlit as st
from database import add_question, load_questions, get_subjects
from pdf_generator import generate_pdf
from datetime import datetime

st.title("📄 Objective Paper Generator")

st.header("Add Question")

subject = st.text_input("Subject (e.g. Math, English)")
question = st.text_area("Question")

col1, col2 = st.columns(2)
with col1:
    option_a = st.text_input("Option A")
    option_b = st.text_input("Option B")
with col2:
    option_c = st.text_input("Option C")
    option_d = st.text_input("Option D")

answer = st.selectbox("Correct Answer", ["A", "B", "C", "D"])

if st.button("Add Question"):
    add_question({
        "subject": subject,
        "question": question,
        "options": {
            "A": option_a,
            "B": option_b,
            "C": option_c,
            "D": option_d
        },
        "answer": answer
    })
    st.success("Question Added!")

st.header("Generate PDF")

subjects = get_subjects()
selected_subject = st.selectbox("Select Subject", ["All"] + subjects)

if st.button("Generate PDFs"):
    data = load_questions()

    if selected_subject != "All":
        data = [q for q in data if q["subject"] == selected_subject]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    q_file = generate_pdf(data, f"questions_{selected_subject}_{timestamp}.pdf", False)
    a_file = generate_pdf(data, f"answers_{selected_subject}_{timestamp}.pdf", True)

    st.success("PDFs Generated!")

    with open(q_file, "rb") as f:
        st.download_button("Download Questions PDF", f)

    with open(a_file, "rb") as f:
        st.download_button("Download Answers PDF", f)
