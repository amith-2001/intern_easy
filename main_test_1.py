import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
import openai
import json
import ast

# MongoDB Connection and User Management
uri = "mongodb+srv://amithdeeplearningworkshop:mucgz8JjD5ynz40A@cluster.uoawthn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.app_users
user_data_collection = db.user_data

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(user_password, hashed_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def sign_up(username, password):
    if user_data_collection.find_one({"username": username}):
        return False
    hashed_pw = hash_password(password)
    user_data_collection.insert_one({"username": username, "password": hashed_pw, "profile": {}})
    return True

def log_in(username, password):
    user = user_data_collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return True
    else:
        return False

# Streamlit App
def profile_form(username):
    with st.form("profile_form"):
        st.write("Profile Information")
        job_interest = st.text_input("Job interest")
        interests = st.text_area("Interests")
        project_description = st.text_area("Project description")
        skills = st.text_input("Skills")
        job_level = st.selectbox("Job level", ["Entry Level", "Internship", "Mid Level", "Senior Level", "Manager"])
        # submitted = st.form_submit_button("Submit")
        if st.form_submit_button("Submit"):
            st.write("Submit button clicked.")
            update_result = user_data_collection.app_users.user_data.username.update_one(
                {"username": username},
                {"$set": {
                    "profile.job_interest": job_interest,
                    "profile.interests": interests,
                    "profile.project_description": project_description,
                    "profile.skills": skills,
                    "profile.job_level": job_level,
                    "profile.knowledge_depth": knowledge depth,
                }},
                upsert=True
            )
            if update_result.modified_count > 0:
                st.success("Profile updated successfully!")
            else:
                st.info("No changes detected or user profile is new.")

def main():
    st.sidebar.title("Authentication")
    choice = st.sidebar.selectbox("Login/Signup", ["Login", "Signup"])

    if choice == "Signup":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Signup"):
            if sign_up(username, password):
                st.success("You are signed up")
                st.balloons()
            else:
                st.error("Username already exists")

    elif choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if log_in(username, password):
                st.success(f"Welcome {username}")
                profile_form(username)
            else:
                st.error("Incorrect username/password")

# OpenAI GPT-3 Question Generation
def generate_questions_for_user(api_key, user_profile):
    openai.api_key = api_key
    prompt_text = f"""Given a user profile with the following details:
- Job interest: {user_profile['job_interest']}
- Interests: {user_profile['interests']}
- Project description: {user_profile['project_description']}
- Skills: {user_profile['skills']}
- Job level: {user_profile['job_level']}
Generate 5 technical questions which increase in difficulty as the question number increases. The first 3 questions should be easy, and the next two can be hard and very hard. Output as JSON only."""
    chat_params = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": prompt_text}]
    }
    response = openai.ChatCompletion.create(**chat_params)
    return response.choices[0].message['content'].strip()

# JSON File Interaction for Questions and Answers
def ask_questions_and_collect_answers(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading from file: {e}")
        return

    for question in data['questions']:
        print(f"\nQuestion ({question['difficulty']}): {question['question']}")
        user_answer = input("Your answer: ")
        question['answer'] = user_answer

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == '__main__':
    # Here you can define logic to run different parts based on your application's needs.
    # For example:
    main()  # To run Streamlit app
    # Note: Uncomment the part you want to run, and ensure you have the necessary environment setup.
