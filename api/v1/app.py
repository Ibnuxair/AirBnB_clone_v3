#!/usr/bin/python3
"""Get the status of the API."""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown_storage(exception):
    """Close the storage when the app context ends"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 status code response."""
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, debug=True, threaded=True)