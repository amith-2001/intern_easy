import streamlit as st
import random

# Assuming default values for demonstration, should ideally come from user input or session state
username = "Amith"
skills = "Python, SQL, AI"
field_interest = "AI"
experience_level = "Intern"

# Theme customization for Streamlit
# st.set_page_config(page_title="My Streamlit App", layout="wide")

# Custom CSS to enhance UI elements
st.markdown(
    """
    <style>
    .main {
        background-color: #008000;
    }
    .stTextInput>div>div>input {
        color: #4f8bf9;
    }
    .stTextArea>div>div>textarea {
        color: #4f8bf9;
    }
    .stSelectbox>div>div>select {
        color: #4f8bf9;
    }
    .reportview-container .markdown-text-container {
        font-family: monospace;
    }
    .widget-container div[role="button"] {
        background-color: #4f8bf9;
        color: white;
    }
    .widget-container div[role="button"]:hover {
        background-color: #3a6fb0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def login():
    st.session_state.page = 'questions'

def submit_questions():
    st.session_state.page = 'test'

def submit_test():
    st.session_state.page = 'result'

def view_profile():
    st.session_state.page = 'profile'

def answer_inputs(questions):
    answers = {}
    for i, question in enumerate(questions, start=1):
        answer = st.text_input(f"Question {i}: {question}", key=f"question_{i}")
        if answer:  # If an answer is provided, store it
            answers[f"question_{i}"] = answer
    return answers

if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Define page navigation
if st.session_state.page == 'login':
    st.image("https://via.placeholder.com/150", width=150)
    st.title("Welcome to the App 🌟")
    username = st.text_input("Username", placeholder="Your Username")
    password = st.text_input("Password", type="password", placeholder="A Secure Password")
    if st.button("Login"):
        login()

elif st.session_state.page == 'questions':
    st.title("📝 Tell Us About Yourself")
    picture = st.camera_input("Take a picture (optional)")
    col1, col2 = st.columns(2)
    with col1:
        skills = st.text_input("What are your skills?", placeholder="e.g., Python, SQL, AI")
    with col2:
        project = st.text_area("Tell us about a project you worked on", placeholder="My project...")
    col3, col4 = st.columns(2)
    with col3:
        field_interest = st.text_input("What field are you interested to work in?", placeholder="e.g., AI")
    with col4:
        experience_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
    if st.button("Submit"):
        submit_questions()

elif st.session_state.page == 'test':
    st.title("💡 Test Questions")
    picture = st.camera_input("Capture an image if needed (optional)")
    questions = ["What is Machine Learning?", "What is the difference between artificial intelligence and machine learning?", "How would you assess the performance of a machine learning model?.","Explain the differences between supervised and unsupervised learning","Can you discuss the pros and cons of using ensemble learning methods in data science?"]
    st.session_state.answers = answer_inputs(questions)
    if st.button("Submit Test"):
        submit_test()

elif st.session_state.page == 'result':
    st.title("✨ Your Test Score")
    score = random.randint(1, 10)
    # Custom circular progress bar for score
    st.markdown(f"""
        <div style="border-radius: 50%; width: 100px; height: 100px; border: 6px solid #4f8bf9; 
                    display: flex; justify-content: center; align-items: center; margin: auto; 
                    font-size: 24px; color: #4f8bf9;">
            {score}/10
        </div>
        """, unsafe_allow_html=True)
    if st.button("View Profile"):
        view_profile()

elif st.session_state.page == 'profile':
    st.title("👤 Your Profile")
    st.markdown(f"""
    - **Username:** {username}
    - **Skills:** {skills}
    - **Field of Interest:** {field_interest}
    - **Experience Level:** {experience_level}
    """)

# For real-world applications, replace placeholders and defaults with dynamic content and user inputs.
