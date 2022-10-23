"""REST API for status."""
import json
import flask
from flask import session
import roomieMatter
import roomieMatter.views.index as index
import roomieMatter.db as db


@roomieMatter.app.route('/api/status', methods=['GET', 'POST'])
def status():
    if not index.auth():
        return flask.Response(status=401)
    context = {}
    if flask.request.method == 'GET':
        context["status"] = db.get_status_db(flask.session['username'])
        return flask.jsonify(**context)
    elif flask.request.method == 'POST':
        context["status"] = db.change_status_db(flask.session['username'])
        return flask.jsonify(**context)

