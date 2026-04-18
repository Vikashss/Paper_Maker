import streamlit as st
from supabase import create_client

# Load secrets safely
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

# Initialize client safely
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= ADD QUESTION =================
def add_question(data):
    try:
        if not supabase:
            return

        supabase.table("questions").insert({
            "subject": data["subject"],
            "question": data["question"],
            "option_a": data["options"]["A"],
            "option_b": data["options"]["B"],
            "option_c": data["options"]["C"],
            "option_d": data["options"]["D"],
            "answer": data["answer"]
        }).execute()

    except Exception as e:
        st.error("❌ Failed to add question. Check database setup.")

# ================= LOAD QUESTIONS =================
def load_questions():
    try:
        if not supabase:
            return []

        response = supabase.table("questions").select("*").execute()

        if not response.data:
            return []

        data = []
        for r in response.data:
            data.append({
                "subject": r.get("subject", ""),
                "question": r.get("question", ""),
                "options": {
                    "A": r.get("option_a", ""),
                    "B": r.get("option_b", ""),
                    "C": r.get("option_c", ""),
                    "D": r.get("option_d", "")
                },
                "answer": r.get("answer", "")
            })

        return data

    except Exception as e:
        st.error("❌ Database connection failed. Check Supabase settings.")
        return []

# ================= GET SUBJECTS =================
def get_subjects():
    data = load_questions()
    return sorted(list(set(q["subject"] for q in data if q["subject"])))
