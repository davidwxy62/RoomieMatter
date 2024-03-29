"""
RoomieMatter index (main) view.
URLs include:
/
/about
/login
/signup
/welcome
/request
/createRoom
/viewRequests
"""
import flask
import roomieMatter
from roomieMatter import db
from roomieMatter import helper

def auth():
    """Check if user is logged in."""
    if not helper.loggedIn(flask.session.get("username", None), flask.request.authorization):
        return False
    if not flask.session.get("username", None):
        flask.session['username'] = flask.request.authorization["username"]
    return True

@roomieMatter.app.route('/')
def show_index():
    """Display / route."""
    if not auth():
        return flask.redirect(flask.url_for('welcome'))
    if flask.session.get("username", None) == "mh988":
        return flask.render_template("secret.html", **context)
    joined = db.is_joined_db(flask.session['username'])
    room_requested = db.join_requested_db(flask.session['username'])
    if not joined and not room_requested:
        return flask.redirect(flask.url_for('start'))
    context = {}
    context['has_pending_requests'] = db.has_pending_requests_db(flask.session['username'])
    context['room_requested'] = room_requested
    return flask.render_template("index.html", **context)

@roomieMatter.app.route('/start')
def start():
    """For users to join/create a room."""
    if not auth():
        return flask.redirect(flask.url_for('welcome'))
    return flask.render_template("start.html")

@roomieMatter.app.route('/about')
def about():
    """Display /about route."""
    return flask.render_template("about.html")

@roomieMatter.app.route('/login')
def login():
    """Login form"""
    return flask.render_template("login.html")

@roomieMatter.app.route('/signup')
def signup():
    """Signup form"""
    context = {}
    return flask.render_template("signup.html", **context)

@roomieMatter.app.route('/welcome')
def welcome():
    """Welcome page"""
    context = {}
    return flask.render_template("welcome.html", **context)


@roomieMatter.app.route('/join', methods=['GET', 'POST'])
def join():
    """Roomie requests."""
    if not auth():
        return flask.redirect(flask.url_for('welcome'))
    context = {}
    context["username"] = flask.session['username']
    if flask.request.method == 'GET':
        return flask.render_template("join.html", **context)
    if flask.request.method == 'POST':
        form = flask.request.form
        roomname = form['roomname']
        if db.request_db(flask.session['username'], roomname):
            return flask.redirect(flask.url_for('show_index'))
        context = {'error': 'Check your spelling and try again.'}
        return flask.render_template('join.html', **context)


@roomieMatter.app.route('/createroom', methods=['GET', 'POST'])
def createroom():
    """Create a room."""
    if not auth():
        return flask.redirect(flask.url_for('welcome'))
    context = {}
    if flask.request.method == 'GET':
        context["username"] = flask.session['username']
        return flask.render_template("createroom.html", **context)
    if flask.request.method == 'POST':
        form = flask.request.form
        roomname = form['roomname']
        if db.create_room_db(flask.session['username'], roomname):
            return flask.redirect(flask.url_for('show_index'))
        return flask.redirect(flask.url_for('createroom'))


@roomieMatter.app.route('/viewrequests')
def viewrequests():
    """View roomie requests."""
    if not auth():
        return flask.redirect(flask.url_for('welcome'))
    context = {}
    context['roomname'] = db.get_roomname_db(flask.session['username'])
    context["username"] = flask.session['username']
    return flask.render_template("viewrequests.html", **context)


