"""REST API for status."""
import json
import flask
import roomieMatter
import roomieMatter.views.index as index
import roomieMatter.db as db


@roomieMatter.app.route('/api/particle')
def particle():
    """Particle API."""
    args = flask.request.args
    if db.username_pwd_match_db(args['username'], args['password']):
        if 'changeTo' in args:
            if db.get_status_db(args['username']) != args['changeTo']:
                db.change_status_db(args['username'])
            return flask.Response(status=204)
        elif 'IP' in args:
            db.update_ip_db(args['username'], args['IP'])
            return flask.Response(status=204)
    return flask.Response(status=401)




@roomieMatter.app.route('/api/status', methods=['GET', 'POST'])
def status():
    if not index.auth():
        return flask.Response(status=401)
    context = {}
    if flask.request.method == 'GET':
        context["status"] = db.get_status_db(flask.session['username'])
        context["name"] = db.get_name_db(flask.session['username'])
        return flask.jsonify(**context)
    elif flask.request.method == 'POST':
        context["status"] = db.change_status_db(flask.session['username'])
        return flask.jsonify(**context)


@roomieMatter.app.route('/api/pendingRequests', methods=['GET', 'DELETE', 'POST'])
def pendingRequests():
    if not index.auth():
        return flask.Response(status=401)
    context = {}
    if flask.request.method == 'GET':
        context["requests"] = db.get_pending_requests_db(flask.session["username"])
        return flask.jsonify(**context)

    elif flask.request.method == 'DELETE':
        form = json.loads(flask.request.data)
        db.delete_pending_requests_db(flask.session["username"], form['senderId'])
        context["senderId"] = form['senderId']
        return flask.jsonify(**context)

    elif flask.request.method == 'POST':
        form = json.loads(flask.request.data)
        print(db.add_roomie_db(flask.session["username"], form['senderId']))
        print(db.delete_pending_requests_db(flask.session["username"], form['senderId']))
        context["senderId"] = form['senderId']
        return flask.jsonify(**context)


@roomieMatter.app.route('/api/roomies', methods=['GET', 'DELETE'])
def roomies():
    if not index.auth():
        return flask.Response(status=401)
    context = {}
    if flask.request.method == 'GET':
        context["roomies"] = db.get_roomies_db(flask.session["username"])
        return flask.jsonify(**context)

    # Do it later
    # elif flask.request.method == 'DELETE':
    #     form = json.loads(flask.request.data)
    #     db.delete_roomie_db(flask.session["username"], form['roomieId'])
    #     context["roomieId"] = form['roomieId']
    #     return flask.jsonify(**context)

