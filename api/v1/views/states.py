#!/usr/bin/python3
"""Handles RESTful API actions for State objects."""
from flask import jsonify, abort, request
from models import storage
from . import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """Retrieves the list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """Retrieves a specific State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a State object."""
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    new_state = State(**req_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route(
    '/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
