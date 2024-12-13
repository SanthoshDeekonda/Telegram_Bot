import pandas as pd
import json


def load_data(path:str):
    return pd.read_csv(path)


def add_data(values:list, data_set):
    data_set.loc[len(data_set)] = values


def save_data(path:str, data_set):
    data_set.to_csv(path)


def load_json_data(path:str)->dict:
    with open(path, 'r') as file:
        data = json.load(file)
    
    return data
