#!/usr/bin/python3
"""
Handles RESTful API actions for User objects.
"""

from flask import jsonify, abort, request
from models import storage
from . import app_views
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Retrieves the list of all User objects."""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Retrieves a specific User object."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a User object."""
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    if 'email' not in req_data:
        abort(400, 'Missing email')
    if 'password' not in req_data:
        abort(400, 'Missing password')
    new_user = User(**req_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Updates a User object."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at', 'password']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
