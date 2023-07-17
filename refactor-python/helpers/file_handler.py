import json
import os


def save_manhwa_data(path, file_name, data):
    output_file_path = os.path.join(path, file_name + ".json")
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file)


def load_manhwa_data(path, file_name):
    input_file_path = os.path.join(path, file_name + ".json")
    with open(input_file_path, "r") as json_file:
        json_data = json.load(json_file)
        return json_data
