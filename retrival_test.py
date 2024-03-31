import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

# MongoDB Connection URI
# Remember to secure your credentials; do not hardcode them in a production environment
uri = "mongodb+srv://amithdeeplearningworkshop:mucgz8JjD5ynz40A@cluster.uoawthn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.app_users
user_data_collection = db.user_data

# Hash and verify password functions as previously defined

# Sign up, log in, and profile form functions as previously defined

# Retrieve profile data
def retrieve_profile_data(username):
    user_data = user_data_collection.find_one({"username": username}, {"_id": 0, "password": 0})  # Exclude password and id from the results
    return user_data.get('profile', {}) if user_data else None

# Display profile data
def display_profile_data(username):
    profile_data = retrieve_profile_data(username)
    if profile_data:
        st.write("Your Profile Data:")
        st.json(profile_data)
    else:
        st.write("No profile data found.")


display_profile_data("Amith")