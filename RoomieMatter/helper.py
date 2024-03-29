"""Helper functions here and there."""
import hashlib
import uuid
from roomieMatter import db

def loggedIn(cookie, auth_obj):
    """Help with both cookie and HTTP basic authorization."""
    if cookie:
        return True

    try:
        auth_user = auth_obj.get("username")
        auth_pwd = auth_obj.get("password")
    except AttributeError:
        return False

    if not auth_user or not auth_pwd:
        return False
    return db.username_pwd_match_db(auth_user, auth_pwd)


def hash_password(password):
    """Hash a password for storing."""
    salt = uuid.uuid4().hex
    pepper = b'\xda\xa1\xcbg\xd3\xddP\x9a\xd6\xa2\xe0\xadP\xe0a.'
    return hashlib.sha512(salt.encode() + password.encode() + pepper).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    """Check hashed password against user's password."""
    password, salt = hashed_password.split(':')
    pepper = b'\xda\xa1\xcbg\xd3\xddP\x9a\xd6\xa2\xe0\xadP\xe0a.'
    return password == hashlib.sha512(salt.encode() + user_password.encode() + pepper).hexdigest()


def newUser(form):
    """Sign up a new user."""
    if form["password1"] != form["password2"]:
        return "Passwords do not match"
    pwd = form["password1"]

    already_exists = db.create_user_db(form['username'], form['name'], form['email'], pwd)
    if already_exists:
        return already_exists
    return None