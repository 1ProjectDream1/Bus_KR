import json

def readFile():
    with open("inPark.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data