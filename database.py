import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_question(data):
    supabase.table("questions").insert({
        "subject": data["subject"],
        "question": data["question"],
        "option_a": data["options"]["A"],
        "option_b": data["options"]["B"],
        "option_c": data["options"]["C"],
        "option_d": data["options"]["D"],
        "answer": data["answer"]
    }).execute()

def load_questions():
    response = supabase.table("questions").select("*").execute()

    return [{
        "subject": r["subject"],
        "question": r["question"],
        "options": {
            "A": r["option_a"],
            "B": r["option_b"],
            "C": r["option_c"],
            "D": r["option_d"]
        },
        "answer": r["answer"]
    } for r in response.data]

def get_subjects():
    data = load_questions()
    return list(set(q["subject"] for q in data))
