#!/usr/bin/python3
"""Get the status of the API."""
from . import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'])
def api_status():
        """Returns a JSON object containing the API status."""
        response = jsonify({'status': 'OK'})
        response.headers['Content-Type'] = 'application/json'

        return response


@app_views.route('/stats', methods=['GET'])
def get_stats():
        """Returns the count of each object type."""
        """Returns the count of each object type."""
        counts = {
                "Amenity": storage.count(Amenity),
                "City": storage.count(City),
                "Place": storage.count(Place),
                "Review": storage.count(Review),
                "State": storage.count(State),
                "User": storage.count(User)
        }
        return jsonify(counts)
