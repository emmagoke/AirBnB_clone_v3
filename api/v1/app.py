#!/usr/bin/python3
"""
This python script contains Blueprint  insrtances and other things.
"""
from flask import Flask
from flask import make_response
from flask import jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ This function handles a session closing. """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """This handles all 404 error. """

    return make_response(jsonify({"error": "Not found"}))


if __name__ == '__main__':
    from os import getenv

    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = int(getenv('HBNB_API_PORT'))
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
