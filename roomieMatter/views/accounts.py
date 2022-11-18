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
        return flask.redirect(flask.url_for('show_index'))

    elif flask.request.form['operation'] == 'signup':
        account_post_create(flask.request.form)
        flask.session['username'] = flask.request.form['username']
        return flask.redirect(flask.url_for('show_index'))

    elif flask.request.form['operation'] == 'changeUsername':
        new_username = flask.request.form['new_username']
        db.change_username_db(flask.session['username'], new_username)
        flask.session['username'] = new_username
        return flask.redirect(flask.url_for('profile'))

    elif flask.request.form['operation'] == 'changeName':
        new_name = flask.request.form['new_name']
        db.change_name_db(flask.session['username'], new_name)
        return flask.redirect(flask.url_for('profile'))

    elif flask.request.form['operation'] == 'changeEmail':
        new_email = flask.request.form['new_email']
        db.change_email_db(flask.session['username'], new_email)
        return flask.redirect(flask.url_for('profile'))

    elif flask.request.form['operation'] == 'changeRoomName':
        new_roomname = flask.request.form['new_roomname']
        db.change_roomname_db(flask.session['username'], new_roomname)
        return flask.redirect(flask.url_for('profile'))

    elif flask.request.form['operation'] == 'exitRoom':
        db.exit_room_db(flask.session['username'])
        return flask.redirect(flask.url_for('show_index'))


@roomieMatter.app.route('/accounts/logout/', methods=['POST'])
def logout_post():
    """Log out a user."""
    flask.session.clear()
    return flask.redirect(flask.url_for('welcome'))


@roomieMatter.app.route('/profile')
def profile():
    """View profile."""
    if not index.auth():
        return flask.redirect(flask.url_for('welcome'))
    name, email, room = db.get_all_info_db(flask.session['username'])
    context = {
        "username": flask.session['username'],
        "name": name,
        "email": email,
        "room": room
    }
    return flask.render_template("profile.html", **context)


@roomieMatter.app.route('/changeUsername', methods=['GET'])
def change_username():
    """Change username."""
    if not index.auth():
        return flask.redirect(flask.url_for('welcome'))
    return flask.render_template("changeUsername.html")


@roomieMatter.app.route('/changeName', methods=['GET'])
def change_name():
    """Change name."""
    if not index.auth():
        return flask.redirect(flask.url_for('welcome'))
    return flask.render_template("changeName.html")


@roomieMatter.app.route('/changeEmail', methods=['GET'])
def change_email():
    """Change email."""
    if not index.auth():
        return flask.redirect(flask.url_for('welcome'))
    return flask.render_template("changeEmail.html")

@roomieMatter.app.route('/changeRoomName', methods=['GET'])
def change_roomname():
    """Change room name."""
    if not index.auth():
        return flask.redirect(flask.url_for('welcome'))
    return flask.render_template("changeRoomName.html")

def account_post_create(form):
    """Sign up a new user."""
    if form["password1"] != form["password2"]:
        flask.abort(400)
    pwd = form["password1"]
    try:
        already_exists = db.create_user_db(form['username'], form['name'], form['email'], pwd)
        if already_exists:
            flask.abort(409)
    except KeyError:
        flask.abort(400)
