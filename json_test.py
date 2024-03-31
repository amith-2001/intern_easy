import json

# Replace 'your_file_path.json' with the path to your JSON file
file_path = 'yale_hack.json'

try:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        print(json.dumps(data, indent=4))  # Print the data formatted as JSON
except Exception as e:
    print(f"Error reading the JSON file: {e}")
