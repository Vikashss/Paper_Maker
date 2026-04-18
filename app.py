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
    if subject and question and option_a and option_b and option_c and option_d:
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
        st.warning("⚠️ Please fill all fields")

# ================= PDF GENERATOR =================
st.header("📄 Generate PDF")

subjects = get_subjects()

if not subjects:
    st.warning("⚠️ No questions available yet")
    selected_subject = "All"
else:
    selected_subject = st.selectbox("Select Subject", ["All"] + subjects)

if st.button("Generate PDFs"):
    data = load_questions()

    if selected_subject != "All":
        data = [q for q in data if q["subject"] == selected_subject]

    if not data:
        st.warning("⚠️ No questions found")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        q_file = generate_pdf(data, f"questions_{timestamp}.pdf", False, selected_subject)
        a_file = generate_pdf(data, f"answers_{timestamp}.pdf", True, selected_subject)

        st.success("✅ PDFs Generated!")

        with open(q_file, "rb") as f:
            st.download_button(
                "📥 Download Questions PDF",
                data=f,
                file_name=f"questions_{timestamp}.pdf",
                mime="application/pdf"
            )

        with open(a_file, "rb") as f:
            st.download_button(
                "📥 Download Answers PDF",
                data=f,
                file_name=f"answers_{timestamp}.pdf",
                mime="application/pdf"
            )

# ================= SSC PRACTICE MODE =================
st.header("🧠 SSC Practice Test")

questions = load_questions()
total_q = len(questions)

if total_q == 0:
    st.warning("⚠️ No questions available. Add questions first.")

else:
    if total_q < 5:
        st.info(f"ℹ️ Only {total_q} question(s) available")

    # FIXED SLIDER ISSUE
    if total_q == 1:
        st.info("Only 1 question available. Test will use it.")
        num_q = 1
    else:
        num_q = st.slider("Number of Questions", 1, total_q, min(10, total_q))

    # START TEST
    if st.button("Start Test"):
        if total_q == 1:
            st.session_state.quiz = questions
        elif total_q < num_q:
            st.session_state.quiz = questions
        else:
            st.session_state.quiz = random.sample(questions, num_q)

        st.session_state.answers = {}
        st.session_state.start_time = time.time()
        st.session_state.submitted = False

# ================= SHOW QUIZ =================
if "quiz" in st.session_state and not st.session_state.get("submitted", False):
    quiz = st.session_state.quiz

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 600 - elapsed)

    st.warning(f"⏱️ Time Left: {remaining} seconds")

    if remaining == 0:
        st.session_state.submitted = True

    for i, q in enumerate(quiz):
        st.write(f"{i+1}. {q['question']}")

        choice = st.radio(
            "Select Answer",
            ["A", "B", "C", "D"],
            key=f"q_{i}"
        )

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

    st.success(f"✅ Final Score: {final_score} / {len(quiz)}")
