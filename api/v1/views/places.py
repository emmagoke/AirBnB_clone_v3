#!/usr/bin/python3
"""
This view handles all default RESTFul API actions for the Place object
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_in_city(city_id):
    """ Retrieves the list of all Place objects of a City. """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place_city = [place.to_dict() for place in city.places]
    return make_response(jsonify(place_city), 200)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object. """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object. """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place. """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a place object. """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    data = request.get_json()
    for item, value in data.items():
        if value not in to_ignore:
            setattr(place, item, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
