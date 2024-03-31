#not working

import streamlit as st
import json
import ast

file = "yale_hack.json"
def load_questions(file):
    try:
        data = json.load(file)
        data = ast.literal_eval(data)
        return data
    except Exception as e:
        st.error(f"Error loading from file: {e}")
        return None

def display_questions(data):
    if data:
        for question in data.get('questions', []):
            q_text = f"{question['question']} (Difficulty: {question['difficulty']})"
            answer = st.text_input(q_text, key=question['question'])
            question['answer'] = answer

def save_answers(data):
    return json.dumps(data, indent=4)

def main():
    st.title("Questionnaire App")

    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    if uploaded_file is not None:
        data = load_questions(uploaded_file)
        if data:
            display_questions(data)
            if st.button("Save Answers"):
                updated_data = save_answers(data)
                st.download_button(label="Download Updated JSON", data=updated_data, file_name="updated_answers.json", mime="application/json")

if __name__ == "__main__":
    main()
