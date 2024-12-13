import dataHandler
from difflib import get_close_matches
from random import choice

def set_respond_data(data_path:str)->tuple:
    data = dataHandler.load_json_data(data_path)
    resp_data = {}
    pattern_data = {}

    for data in data["intents"]:
        resp_data[data["tag"]] = data["responses"]
        pattern_data[data["tag"]] = [pattern.lower() for pattern in data["patterns"]]
    return pattern_data,resp_data

def get_intent(user_message:str, patterns:dict)-> str or None:
    
    for intent in patterns:
            matches = get_close_matches(user_message, patterns[intent], n=1, cutoff=0.7)
            if matches:
                return intent

    return None    

pattern, resp = set_respond_data("Bot_data/intents.json")

def get_response(user_message:str, patterns:dict, responses:dict)->str:
    intent = get_intent(user_message.lower(), patterns)
    Scope_Clarification = "I'm here to assist with specific tasks and basic conversations, but I may not be the best at extended chatting—thank you for understanding!" 
    if intent is not None:
        return choice(responses[intent])
     
    return Scope_Clarification