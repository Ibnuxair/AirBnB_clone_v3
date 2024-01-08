#!/usr/bin/python3
"""Get the status of the API."""
from . import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def api_status():
        """Returns a JSON object containing the API status."""
        response = jsonify({'status': 'OK'})
        response.headers['Content-Type'] = 'application/json'

        return response
