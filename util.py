import json


def prepare_data(file_path):

    data = json.load(open(file_path, 'r', encoding='utf-8'))

    patterns = []
    tags = []
    responses = {}

    for intent in data['intents']:
        for pattern in intent['patterns']:
            patterns.append(pattern.lower())
            tags.append(intent['tag'])
        responses[intent['tag']] = intent['responses']

    return patterns, tags, responses


   
