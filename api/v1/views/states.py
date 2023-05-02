#!/usr/bin/python3
"""
This view handles all default RESTFul API actions for the STate object
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort
from models import storage
from models.state import State
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """This method Retrieves the list of all State objects. """

    all_states = storage.all(State)
    all_dict = [all_states[state].to_dict() for state in all_states]
    return make_response(jsonify(all_dict), 200)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """ Retrieves a State object. """

    state = ''
    try:
        state = storage.get(State, state_id)
    except Exception:
        pass
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object. """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State. """

    if not request.get_json():
        return abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        return abort(400, description="Missing name")
    state_info = request.get_json()

    new_state = State(**state_info)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object. """

    state = storage.get(State, state_id)

    if not state:
        abort(404)
    if not request.get_json():
        return abort(400, "Not a JSON")

    to_ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for item, value in data.items():
        if item not in to_ignore:
            setattr(state, item, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
