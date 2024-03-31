import openai
import json
def generate_questions_for_user(api_key, user_profile):
    # Set your OpenAI API key
    openai.api_key = api_key

    # Define the prompt with user profile information to generate questions
    prompt_text = f"""Given a user profile with the following details:
- Job interest: {user_profile['job_interest']}
- Interests: {user_profile['interests']}
- Project description: {user_profile['project_description']}
- Skills: {user_profile['skills']}
- Job level: {user_profile['job_level']}
Generate 5 technical questions , which increases in difficulty as the question number increases.The first 3 questions shoul be easy and the next two can be hard and very hard  output as json only."""

    # Define the parameters for the chat completion
    chat_params = {
        "model": "gpt-3.5-turbo",  # Specify the chat model you're using
        "messages": [{
            "role": "system",
            "content": prompt_text
        }]
    }

    # Call the chat completion API
    response = openai.ChatCompletion.create(**chat_params)

    # Return the generated response
    return response.choices[0].message['content'].strip()

# User's profile information
user_profile = {
    "job_interest": "Data Science",
    "interests": "Machine Learning, AI",
    "project_description": "Developed a forecasting model",
    "skills": "Python, R, SQL",
    "job_level": "Mid Level"
}

# Your OpenAI API key (replace with your actual API key)
api_key = "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"

# Generate questions for the user based on their profile


# print(questions)



def running():

    questions = generate_questions_for_user(api_key, user_profile)

    with open("yale_hack_1.json", 'w') as json_file:
        json.dump(questions, json_file, indent=0)
    with open("yale_hack.json", 'w') as json_file:
        json.dump(questions, json_file, indent=0)

running()