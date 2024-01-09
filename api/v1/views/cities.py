#!/usr/bin/python3
"""Handles RESTful API actions for City objects."""
from flask import jsonify, abort, request
from models import storage
from . import app_views
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route(
    '/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Retrieves a specific City object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Creates a City object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    new_city = City(**req_data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route(
    '/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Updates a City object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
