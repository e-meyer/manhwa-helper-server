import json
import os
from flask import Flask, jsonify
from flask import request
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    response = {
        "status": 404,
        "message": "Route not found"
    }
    return jsonify(response), 404


@app.route('/asura', methods=['GET'])
def asura():
    query = request.args.get('query')

    if query is None:
        response = {
            "status": 400,
            "message": "Query parameter is required"
        }
        return jsonify(response), 400

    json_data = load_manhwa_data("Asura")
    found_items = search_titles(query, json_data)

    results = []

    for item in found_items:
        results.append(item)

    return results


@app.route('/flame', methods=['GET'])
def flame():
    query = request.args.get('query')

    if query is None:
        response = {
            "status": 400,
            "message": "Query parameter is required"
        }
        return jsonify(response), 400

    json_data = load_manhwa_data("Flame")
    found_items = search_titles(query, json_data)

    results = []

    for item in found_items:
        results.append(item)

    return results


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
