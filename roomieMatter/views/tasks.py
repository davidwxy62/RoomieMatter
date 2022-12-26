"""
RoomieMatter tasks related view.
URLs include:
/tasks

"""
import flask
import roomieMatter
from roomieMatter import db
from roomieMatter.views import index
from roomieMatter import helper

@roomieMatter.app.route('/tasks')
def tasks():
    """Doc string."""
    if not index.auth():
        return flask.redirect(flask.url_for('index.welcome'))
    return flask.render_template("tasks.html")