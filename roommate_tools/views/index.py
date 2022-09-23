"""
roommate tools index (main) view.
URLs include:
/
"""
import flask
import roommate_tools
@roommate_tools.app.route('/')
def show_index():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)