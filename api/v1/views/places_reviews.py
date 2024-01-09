#!/usr/bin/python3
"""Handles RESTful API actions for Review objects."""
from flask import jsonify, abort, request
from models import storage
from . import app_views
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route(
    '/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route(
    '/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Retrieves a specific Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>', strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Creates a Review object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_data:
        abort(400, 'Missing user_id')
    if 'text' not in req_data:
        abort(400, 'Missing text')
    user = storage.get(User, req_data['user_id'])
    if not user:
        abort(404)
    new_review = Review(**req_data)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Updates a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
