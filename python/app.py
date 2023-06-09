import json
import os
from flask import Flask, jsonify
from flask import request

from helpers.search_titles import search_titles


app = Flask(__name__)


@app.route('/scanlator/<scanlator_name>', methods=['GET'])
def get_scanlator_data(scanlator_name):
    supported_scanlators = ['asura', 'flame', 'luminous', 'reaper']

    search = request.args.get('s')

    # If there is no query
    if not search:
        return jsonify({'error': 'Search parameter is required'}), 400

    # If the scanlator is not supported
    if scanlator_name.lower() not in supported_scanlators:
        return jsonify({'error': 'Scanlator not supported'}), 400

    file_path = os.path.join('data', f'{scanlator_name}.json')

    # If there is no data for the selected scanlator
    if not os.path.exists(file_path):
        return jsonify({'error': 'Data for scanlator not found'}), 404
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)

            query_data = search_titles(search, data)

            return query_data


@app.errorhandler(404)
def not_found(error):
    response = {
        "status": 404,
        "message": "Route not found"
    }
    return jsonify(response), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
