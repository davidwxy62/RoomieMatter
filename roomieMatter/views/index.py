"""
roomieMatter index (main) view.
URLs include:
/
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
    context = {}
    context["username"] = flask.session['username']
    context['joined'] = db.is_joined_db(flask.session['username'])
    if context['joined']:
        context["roomies"] = db.get_roomies_db(flask.session['username'])
    if flask.session.get("username", None) == "Abby":
        return flask.render_template("secret.html", **context)
    user_status = ''
    for d in context['roomies']:
        if d['username'] == flask.session['username']:
            user_status = d['status']
    user_dict = {'username': flask.session['username'], 'status': user_status}
    context['roomies'].remove(user_dict)
    context['roomies'].sort(key=lambda x: x['username'])
    context['roomies'] = [user_dict] + context['roomies']
    return flask.render_template("index.html", **context)

@roomieMatter.app.route('/login')
def login():
    """Login form"""
    context = {}
    return flask.render_template("login.html", **context)

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


@roomieMatter.app.route('/request', methods=['GET', 'POST'])
def request():
    """Roomie requests."""
    if not auth():
        return flask.redirect(flask.url_for('welcome'))
    context = {}
    if flask.request.method == 'GET':
        return flask.render_template("request.html", **context)
    if flask.request.method == 'POST':
        form = flask.request.form
        roomname = form['roomname']
        if db.request_db(flask.session['username'], roomname):
            return flask.redirect(flask.url_for('show_index'))
        return flask.redirect(flask.url_for('request'))


@roomieMatter.app.route('/createroom', methods=['GET', 'POST'])
def createroom():
    """Create a room."""
    if not auth():
        return flask.redirect(flask.url_for('welcome'))
    context = {}
    if flask.request.method == 'GET':
        return flask.render_template("createroom.html", **context)
    if flask.request.method == 'POST':
        form = flask.request.form
        roomname = form['roomname']
        if db.create_room_db(flask.session['username'], roomname):
            return flask.redirect(flask.url_for('show_index'))
        return flask.redirect(flask.url_for('createroom'))