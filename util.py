import json

def prepare_data(file_path):

    with open(file_path, 'r') as file:
        data = json.load(file)

    
    patterns = []
    tags = []
    responses = {}

    for intent in data["intents"]:
        for i in intent["patterns"]:
            patterns.append(i)
            tags.append(intent["tag"])
            responses[intent["tag"]] = intent["responses"]

    return patterns, tags, responses

def load_user_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    file_path = 'intents.json'
    p, t, r = prepare_data(file_path)
    print("Data preparation complete.")