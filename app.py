import streamlit as st
from database import add_question, load_questions, get_subjects
from pdf_generator import generate_pdf
from datetime import datetime
import random
import time

st.set_page_config(page_title="SSC Practice App")

st.title("📄 SSC Objective Paper Generator")

# ================= ADD QUESTION =================
st.header("➕ Add Question")

subject = st.text_input("Subject")
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
    if subject and question:
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
        st.success("✅ Question Added!")
    else:
        st.warning("Fill all fields")

# ================= PDF GENERATOR =================
st.header("📄 Generate PDF")

subjects = get_subjects()
selected_subject = st.selectbox("Select Subject", ["All"] + subjects)

if st.button("Generate PDFs"):
    data = load_questions()

    if selected_subject != "All":
        data = [q for q in data if q["subject"] == selected_subject]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    q_file = generate_pdf(data, f"questions_{timestamp}.pdf", False, selected_subject)
    a_file = generate_pdf(data, f"answers_{timestamp}.pdf", True, selected_subject)

    st.success("PDF Ready!")

    with open(q_file, "rb") as f:
        st.download_button("Download Questions PDF", f)

    with open(a_file, "rb") as f:
        st.download_button("Download Answers PDF", f)

# ================= SSC PRACTICE MODE =================
st.header("🧠 SSC Practice Test")

questions = load_questions()

if questions:
    num_q = st.slider("Number of Questions", 5, min(50, len(questions)), 10)

    if st.button("Start Test"):
        st.session_state.quiz = random.sample(questions, num_q)
        st.session_state.answers = {}
        st.session_state.start_time = time.time()
        st.session_state.submitted = False

if "quiz" in st.session_state and not st.session_state.get("submitted", False):
    quiz = st.session_state.quiz

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 600 - elapsed)

    st.warning(f"⏱️ Time Left: {remaining} sec")

    if remaining == 0:
        st.session_state.submitted = True

    for i, q in enumerate(quiz):
        st.write(f"{i+1}. {q['question']}")

        choice = st.radio("Answer", ["A","B","C","D"], key=f"q{i}")
        st.session_state.answers[i] = choice

    if st.button("Submit Test"):
        st.session_state.submitted = True

# ================= RESULT =================
if st.session_state.get("submitted"):
    quiz = st.session_state.quiz
    answers = st.session_state.answers

    score = 0
    negative = 0

    st.subheader("📊 Result")

    for i, q in enumerate(quiz):
        correct = q["answer"]
        user_ans = answers.get(i)

        if user_ans == correct:
            score += 1
        else:
            negative += 0.25

        st.write(f"Q{i+1}: Your: {user_ans} | Correct: {correct}")

    final_score = score - negative

    st.success(f"Final Score: {final_score}/{len(quiz)}")
