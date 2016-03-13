#!/usr/bin/env python3

"""Initial tests for git as data backend. Creates a data storage, which prints the location of the git repository. Then sleeps forever.
"""

from datastore import Datastore
import time

import flask
import jsonapi
import jsonapi.flask

api = flask.Flask(__name__)
api = jsonapi.flask.FlaskAPI("/api", db=...,  flask_app=app)

if __name__=='__main__':
    with Datastore() as ds:
        ds.addTransaction(2016, 'test')
        while True:
            time.sleep(2)
