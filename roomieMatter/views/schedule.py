"""
RoomieMatter schedule related view.
URLs include:
/schedule

"""
import flask
import roomieMatter
from roomieMatter import db
from roomieMatter.views import index
from roomieMatter import helper

@roomieMatter.app.route('/schedule')
def schedule():
    """Doc string."""
    if not index.auth():
        return flask.redirect(flask.url_for('welcome'))
    return flask.render_template("schedule.html")