#!/usr/bin/python3
"""
This view handles all default RESTFul API actions for the City object
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_in_states(state_id):
    """ Retrieves the list of all City objects of a State. """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    city_state = [ city.to_dict() for city in state.cities]
    return make_response(jsonify(city_state), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object. """

    city  = storage.get(City, city_id)
    if city is None:
        abort(404)

    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object. """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City. """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    city = City(**data)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object. """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()
    for item, value in data.items():
        if value not in to_ignore:
            setattr(city, item, value)
    return make_response(jsonify(city.to_dict()), 200)
