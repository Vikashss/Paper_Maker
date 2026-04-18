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
        st.warning("⚠️ Fill all fields")

# ================= PDF =================
st.header("📄 Generate PDF")

subjects = get_subjects()
selected_subject = st.selectbox("Select Subject", ["All"] + subjects if subjects else ["All"])

if st.button("Generate PDFs"):
    data = load_questions()

    if selected_subject != "All":
        data = [q for q in data if q["subject"] == selected_subject]

    if data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        q_file = generate_pdf(data, f"questions_{timestamp}.pdf", False, selected_subject)
        a_file = generate_pdf(data, f"answers_{timestamp}.pdf", True, selected_subject)

        with open(q_file, "rb") as f:
            st.download_button("📥 Questions PDF", f, f"questions_{timestamp}.pdf", "application/pdf")

        with open(a_file, "rb") as f:
            st.download_button("📥 Answers PDF", f, f"answers_{timestamp}.pdf", "application/pdf")
    else:
        st.warning("No data found")

# ================= PRACTICE =================
st.header("🧠 Practice Mode")

questions = load_questions()
total_q = len(questions)

if total_q > 0:

    if total_q == 1:
        num_q = 1
    else:
        num_q = st.slider("Questions", 1, total_q, min(10, total_q))

    if st.button("Start Practice"):
        st.session_state.quiz = random.sample(questions, num_q) if total_q >= num_q else questions
        st.session_state.answers = {}
        st.session_state.submitted = False

if "quiz" in st.session_state and not st.session_state.get("submitted"):
    for i, q in enumerate(st.session_state.quiz):
        st.write(f"{i+1}. {q['question']}")
        choice = st.radio("Answer", ["A","B","C","D"], key=f"p{i}")
        st.session_state.answers[i] = choice

    if st.button("Submit Practice"):
        st.session_state.submitted = True

if st.session_state.get("submitted"):
    score = 0
    for i, q in enumerate(st.session_state.quiz):
        if st.session_state.answers.get(i) == q["answer"]:
            score += 1
    st.success(f"Score: {score}/{len(st.session_state.quiz)}")

# ================= SSC FULL TEST =================
st.header("🏆 SSC Full Test (Testbook Style)")

sections = {
    "Reasoning": [q for q in questions if "reason" in q["subject"].lower()],
    "GK": [q for q in questions if "gk" in q["subject"].lower()],
    "Math": [q for q in questions if "math" in q["subject"].lower()],
    "English": [q for q in questions if "english" in q["subject"].lower()]
}

if st.button("Start SSC Test"):
    st.session_state.section_names = list(sections.keys())
    st.session_state.section_index = 0
    st.session_state.q_index = 0
    st.session_state.answers = {}
    st.session_state.start_time = time.time()

# ================= TEST UI =================
if "section_index" in st.session_state:

    # FINISH TEST
    if st.session_state.section_index >= len(sections):
        st.header("📊 Result")

        score = 0
        neg = 0

        for v in st.session_state.answers.values():
            if v["selected"] == v["correct"]:
                score += 1
            else:
                neg += 0.25

        st.success(f"Final Score: {score - neg}")
        st.stop()

    section = st.session_state.section_names[st.session_state.section_index]
    qs = sections[section]

    # SKIP EMPTY SECTION SAFELY
    if not qs:
        st.warning(f"No questions in {section}, skipping...")
        st.session_state.section_index += 1
        st.rerun()

    st.subheader(f"📘 {section}")

    # TIMER
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 900 - elapsed)

    st.warning(f"⏱️ {remaining} sec left")

    if remaining == 0:
        st.session_state.section_index += 1
        st.session_state.q_index = 0
        st.session_state.start_time = time.time()
        st.rerun()

    i = st.session_state.q_index
    q = qs[i]

    st.write(f"Q{i+1}. {q['question']}")

    key = f"{section}_{i}"

    choice = st.radio("Answer", ["A","B","C","D"], key=key)

    st.session_state.answers[key] = {
        "selected": choice,
        "correct": q["answer"]
    }

    # NAVIGATION
    col1, col2, col3 = st.columns(3)

    if col1.button("⬅ Prev") and i > 0:
        st.session_state.q_index -= 1
        st.rerun()

    if col2.button("Next ➡") and i < len(qs)-1:
        st.session_state.q_index += 1
        st.rerun()

    if col3.button("Next Section"):
        st.session_state.section_index += 1
        st.session_state.q_index = 0
        st.session_state.start_time = time.time()
        st.rerun()

    # QUESTION PALETTE
    st.markdown("### 🧭 Palette")

    cols = st.columns(10)

    for idx in range(len(qs)):
        k = f"{section}_{idx}"
        color = "🟢" if k in st.session_state.answers else "🔴"

        if cols[idx % 10].button(f"{color} {idx+1}"):
            st.session_state.q_index = idx
            st.rerun()
