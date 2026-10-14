import json

def readFile(fileName):
    with open(fileName, "r", encoding="utf-8") as file:
        content = file.read()
        if not content.split():
            return []
    return json.loads(content)

def wrete_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
