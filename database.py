import json
import os

FILE_PATH = "data/questions.json"

def load_questions():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_questions(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

def add_question(question_data):
    data = load_questions()
    data.append(question_data)
    save_questions(data)

def get_subjects():
    data = load_questions()
    return list(set(q["subject"] for q in data))
