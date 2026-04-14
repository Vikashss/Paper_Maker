import json
import os

FILE_PATH = "data/questions.json"

def ensure_data_file():
    # Create folder if not exists
    os.makedirs("data", exist_ok=True)

    # Create file if not exists
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)

def load_questions():
    ensure_data_file()
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_questions(data):
    ensure_data_file()
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

def add_question(question_data):
    data = load_questions()
    data.append(question_data)
    save_questions(data)

def get_subjects():
    data = load_questions()
    return list(set(q["subject"] for q in data))
