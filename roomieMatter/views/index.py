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
    if flask.session.get("username", None) == "Abby":
        return flask.render_template("secret.html", **context)
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