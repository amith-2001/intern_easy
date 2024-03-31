import json
import ast

def ask_questions_and_collect_answers(file_path):
    # Attempt to load the questions from the specified JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(file)
            data = json.load(file)
            data = ast.literal_eval(data)
            print(type(data))
            # data = dict(data)
    except Exception as e:
        print(f"Error loading from file: {e}")
        return

    # Prompt the user for answers to each question
    for question in data.get('questions'):
        print(f"\nQuestion ({question['difficulty']}): {question['question']}")
        user_answer = input("Your answer: ")
        question['answer'] = user_answer  # Append the user's answer

    # Attempt to write the updated data back to the JSON file
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing to file: {e}")

# Specify the path to your JSON file
file_path = 'yale_hack.json'  # Update this path
ask_questions_and_collect_answers(file_path)

print("The JSON file has been updated with your responses.")
