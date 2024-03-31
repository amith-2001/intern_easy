import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

# MongoDB Connection
uri = "mongodb+srv://amithdeeplearningworkshop:mucgz8JjD5ynz40A@cluster.uoawthn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.app_users
user_data_collection = db.user_data

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def update_user_information(username, job_interest, interests, project_description, skills, job_level):
    # Update operation
    update_result = user_data_collection.update_one(
        {"username": username},
        {"$set": {
            "profile.job_interest": job_interest,
            "profile.interests": interests,
            "profile.project_description": project_description,
            "profile.skills": skills,
            "profile.job_level": job_level
        }}
    )

    return update_result.modified_count > 0

def user_profile_form():
    st.title("Update Your Profile")

    username = st.text_input("Username", help="Enter your username")
    job_interest = st.text_input("Job Interest", help="Type of job you're interested in")
    interests = st.text_area("Interests", help="Your interests")
    project_description = st.text_area("Project Description", help="Describe a project you've worked on")
    skills = st.text_input("Skills", help="Your skills")
    job_level = st.selectbox("Job Level", ["Entry Level", "Internship", "Mid Level", "Senior Level", "Manager", "Not Specified"], help="Enter your desired job level")

    submit_button = st.button("Update Profile")

    if submit_button:
        if update_user_information(username, job_interest, interests, project_description, skills, job_level):
            st.success("Your information has been updated successfully.")
        else:
            st.error("No updates made. Ensure the username exists and changes were made.")

if __name__ == '__main__':
    user_profile_form()
