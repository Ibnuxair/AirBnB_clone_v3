#!/usr/bin/python3
"""Handles RESTful API actions for Amenity objects."""
from flask import jsonify, abort, request
from models import storage
from . import app_views
from models.amenity import Amenity

@app_views.route(
    '/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    amenities = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates an Amenity object."""
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**req_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
