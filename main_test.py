import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
import json
import ast
from questions_generator import running
# MongoDB Connection URI
# Make sure to use environment variables or Streamlit secrets for MongoDB credentials in production
uri = "mongodb+srv://amithdeeplearningworkshop:mucgz8JjD5ynz40A@cluster.uoawthn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.app_users
user_data_collection = db.user_data


# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


# Verify password
def verify_password(user_password, hashed_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)


# Sign up user
def sign_up(username, password):
    if user_data_collection.find_one({"username": username}):
        return False  # User already exists
    hashed_pw = hash_password(password)
    user_data_collection.insert_one({"username": username, "password": hashed_pw, "profile": {}})
    return True


# Log in user
def log_in(username, password):
    user = user_data_collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return True
    else:
        return False


# Profile form
def profile_form(username):
    with st.form("profile_form", clear_on_submit=True):
        st.write("Profile Information")
        job_interest = st.text_input("Job interest")
        interests = st.text_area("Interests")
        project_description = st.text_area("Project description")
        skills = st.text_input("Skills")
        job_level = st.selectbox("Job level", ["Entry Level", "Internship", "Mid Level", "Senior Level", "Manager"])

        submitted = st.form_submit_button("Submit")
        if submitted:
            running()
            ask_questions_and_collect_answers('yale_hack_1.json')
            # try:
            #     # Use $set to only update the 'profile' field of the user document
            #     update_result = user_data_collection.update_one(
            #         {"username": username},
            #         {"$set": {
            #             "profile.job_interest": job_interest,
            #             "profile.interests": interests,
            #             "profile.project_description": project_description,
            #             "profile.skills": skills,
            #             "profile.job_level": job_level
            #         }},
            #         upsert=True
            #     )

            #     if update_result.modified_count > 0:
            #         st.success("Profile updated successfully!")
            #           # Call to show questions after profile update
            #     else:
            #         st.info("No changes detected or user profile is new.")
            # except Exception as e:
            #     st.error(f"An error occurred: {e}")


# Function to ask questions and collect answers
def ask_questions_and_collect_answers(file_path):
    # Load questions from the specified JSON file
    try:


        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data = ast.literal_eval(data)

    except Exception as e:
        st.error(f"Error loading from file: {e}")
        return

    # Display questions and collect answers
    # answers = []
    with st.form("question_form"):
        answers = []
        for question in data.get('questions'):
            answer = st.text_input(f"Question ({question['difficulty']}): {question['question']}", key=question['question'])
            answers.append(answer)

    if st.button('Submit Answers'):
        # Update the data with answers
        for i, question in enumerate(data.get('questions')):
            question["answer"] = answers[i]

        # Save the updated data to a new file
        try:
            with open('yale_hack_2.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            st.success("Thank you for submitting your answers. The file has been updated.")
        except Exception as e:
            st.error(f"Error writing to file: {e}")

        # Here you could save the answers to a database or perform another action
def home():
    st.write('HOME')

# Main app logic
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
                profile_form(username)
            else:
                st.error("Username already exists")

    elif choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if log_in(username, password):
                st.success(f"Welcome {username}")
                ask_questions_and_collect_answers('yale_hack_1.json')
            else:
                st.error("Incorrect username/password")


if __name__ == '__main__':
    main()
