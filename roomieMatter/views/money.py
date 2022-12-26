"""
RoomieMatter money related view.
URLs include:
/money

"""
import flask
import roomieMatter
from roomieMatter import db
from roomieMatter.views import index
from roomieMatter import helper

@roomieMatter.app.route('/money')
def money():
    """Doc string."""
    if not index.auth():
        return flask.redirect(flask.url_for('welcome'))
    return flask.render_template("money.html")