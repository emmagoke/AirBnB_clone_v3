#!/usr/bin/python3
"""
This script contains routes based on app_views
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """This method handles the status(/status) route. """
    return jsonify({
        "status":  "OK"
        })


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ This method returns the count of all the object in the database """

    stat = {"amenities": 0, "cities": 0, "places": 0, "reviews": 0,
            "states": 0, "users": 0}
    stat["amenities"] = stat.get("amenities") + storage.count(Amenity)
    stat["cities"] = stat.get("cities") + storage.count(City)
    stat["places"] = stat.get("places") + storage.count(Place)
    stat["reviews"] = stat.get("reviews") + storage.count(Review)
    stat["states"] = stat.get("states") + storage.count(State)
    stat["users"] = stat.get("users") + storage.count(User)

    return jsonify(stat)
