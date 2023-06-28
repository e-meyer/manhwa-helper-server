import json
import os
from flask import Flask, jsonify
from flask import request


app = Flask(__name__)


@app.route('/scanlator/<scanlator_name>', methods=['GET'])
def get_scanlator_data(scanlator_name):
    supported_scanlators = ['asura', 'flame', 'luminous', 'reaper']

    search = request.args.get('s')

    if not search:
        return jsonify({'error': 'Search parameter is required'}), 400

    file_path = os.path.join('data', f'{scanlator_name}.json')

    if scanlator_name.lower() not in supported_scanlators:
        return jsonify({'error': 'Scanlator not supported'}), 400
    elif not os.path.exists(file_path):
        return jsonify({'error': 'Data for scanlator not found'}), 404
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)

            manhwa_data = search_titles(search, data)

            return manhwa_data


@app.errorhandler(404)
def not_found(error):
    response = {
        "status": 404,
        "message": "Route not found"
    }
    return jsonify(response), 404


def search_titles(query, data):
    results = []
    for item in data["manhwa_data"]:
        if query.lower() in item["title"].lower():
            results.append(item)
    return results


def load_manhwa_data(file_name):
    input_file_path = os.path.join("data", file_name + ".json")
    with open(input_file_path, "r") as json_file:
        json_data = json.load(json_file)
        return json_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
