"""
Insta485 account related view.

URLs related to /acounts/.
"""
import flask
import roomieMatter
from roomieMatter import db
from roomieMatter.views import index


@roomieMatter.app.route('/accounts/', methods=['GET', 'POST'])
def accounts():
    """Doc string."""
    if flask.request.method != 'POST':
        return flask.redirect(flask.url_for('show_index'))

    if flask.request.form['operation'] == 'login':
        form = flask.request.form
        if len(form['username'])*len(form['password']) == 0 or not db.username_pwd_match(form['username'], form['password']):
            context = {"error": "Try different usernames or passwords"}
            return flask.render_template("login.html", **context)
        flask.session['username'] = form['username']
        return flask.redirect(flask.url_for('show_index'))

    elif flask.request.form['operation'] == 'signup':
        error = account_post_create(flask.request.form)
        if error:
            context = {"error": error}
            return flask.render_template("signup.html", **context)
        flask.session['username'] = flask.request.form['username']
        return flask.redirect(flask.url_for('show_index'))

    elif flask.request.form['operation'] == 'changeUsername':
        new_username = flask.request.form['new_username']
        error = db.change_username_db(flask.session['username'], new_username)
        if error:
            context = {"error": error}
            return flask.render_template("changeUsername.html", **context)
        flask.session['username'] = new_username
        return flask.redirect(flask.url_for('profile'))

    elif flask.request.form['operation'] == 'changeName':
        new_name = flask.request.form['new_name']
        error = db.change_name_db(flask.session['username'], new_name)
        if error:
            context = {"error": error}
            return flask.render_template("changeName.html", **context)
        return flask.redirect(flask.url_for('profile'))

    elif flask.request.form['operation'] == 'changeEmail':
        new_email = flask.request.form['new_email']
        error = db.change_email_db(flask.session['username'], new_email)
        if error:
            context = {"error": error}
            return flask.render_template("changeEmail.html", **context)
        return flask.redirect(flask.url_for('profile'))

    elif flask.request.form['operation'] == 'changeRoomName':
        new_roomname = flask.request.form['new_roomname']
        error = db.change_roomname_db(flask.session['username'], new_roomname)
        if error:
            context = {"error": error}
            return flask.render_template("changeRoomName.html", **context)
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
        return "Passwords do not match"
    pwd = form["password1"]

    already_exists = db.create_user_db(form['username'], form['name'], form['email'], pwd)
    if already_exists:
        return already_exists
    return None

