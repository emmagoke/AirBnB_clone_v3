#!/usr/bin/python3
"""
This python script handles all default RESTFul API actions for Amenity object
"""
from api.v1.views import app_views
from flask import make_response, abort, request, jsonify
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects. """

    amenities = storage.all(Amenity)
    all_amenities = [amenities[item].to_dict() for item in amenities]
    return make_response(jsonify(all_amenities), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object. """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object. """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a Amenity. """

    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity object. """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'created_at', 'updated_at']
    for item, value in request.get_json().items():
        if item not in to_ignore:
            setattr(amenity, item, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
