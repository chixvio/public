import json

def write_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data