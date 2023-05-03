#!/usr/bin/python3
"""
This view handles all default RESTFul API actions for the Review object
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_in_place(place_id):
    """ Retrieves the list of all Review objects of a Place. """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review_place = [review.to_dict() for review in place.reviews]
    return make_response(jsonify(review_place), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object. """

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object. """

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review. """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data = request.get_json()
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object. """

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    data = request.get_json()
    for item, value in data.items():
        if value not in to_ignore:
            setattr(review, item, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
