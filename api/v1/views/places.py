#!/usr/bin/python3
"""Handles RESTful API actions for Place objects."""
from flask import jsonify, abort, request
from models import storage
from . import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    '/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route(
    '/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieves a specific Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Creates a Place object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    required_keys = ['user_id', 'name']
    for key in required_keys:
        if key not in req_data:
            abort(400, f"Missing {key}")
    user_id = req_data['user_id']
    if not storage.get(User, user_id):
        abort(404)
    new_place = Place(**req_data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(
    '/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
