#!/usr/bin/python3
"""
This script contains routes based on app_views
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """This method handles the status(/status) route. """
    return jsonify({
        "status":  "OK"
        })
