"""
Insta485 account related view.

URLs related to /acounts/.
"""
import flask
import roomieMatter
from roomieMatter import db
from roomieMatter.views import index


@roomieMatter.app.route('/accounts/', methods=['POST'])
def account_post():
    """Doc string."""
    if flask.request.form['operation'] == 'login':
        form = flask.request.form
        if len(form['username'])*len(form['password']) == 0:
            flask.abort(400)
        if not db.username_pwd_match(form['username'], form['password']):
            flask.abort(403)
        flask.session['username'] = form['username']

    elif flask.request.form['operation'] == 'signup':
        account_post_create(flask.request.form)
        flask.session['username'] = flask.request.form['username']
        context = {}
        return flask.render_template("newuser.html", **context)

    # elif flask.request.form['operation'] == 'delete':
    #     if 'username' not in flask.session:
    #         flask.abort(403)
    #     db.delete_account_db(flask.session['username'])
    #     flask.session.clear()

    # elif flask.request.form['operation'] == 'edit_account':
    #     if 'username' not in flask.session:
    #         flask.abort(403)
    #     account_post_edit(
    #         flask.session['username'],
    #         flask.request.form,
    #         flask.request.files.get('file')
    #     )

    # elif flask.request.form['operation'] == 'update_password':
    #     if 'username' not in flask.session:
    #         flask.abort(403)
    #     account_post_update_pw(
    #         flask.session['username'],
    #         flask.request.form
    #     )

    # if not flask.request.args.get('target'):
    return flask.redirect(flask.url_for('show_index'))
    # return flask.redirect(flask.request.args.get('target'))


@roomieMatter.app.route('/accounts/logout/', methods=['POST'])
def logout_post():
    """Log out a user."""
    flask.session.clear()
    return flask.redirect(flask.url_for('welcome'))


def account_post_create(form):
    """Sign up a new user."""
    if form["password1"] != form["password2"]:
        flask.abort(400)
    pwd = form["password1"]
    try:
        already_exists = db.create_user_db(form['username'], form['email'], pwd)
        if already_exists:
            flask.abort(409)
    except KeyError:
        flask.abort(400)
