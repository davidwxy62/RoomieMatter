"""Helpers related to sql querying."""
from flask import url_for
from roomieMatter.model import get_db

def username_pwd_match(username, pwd):
    """
    Take in username and pw input from current user.

    If the password is right, login the user.
    """
    connection = get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )

    user = cur.fetchone()
    if not user:
        return False
    if 'password' in user:
        return user['password'] == pwd
    return False

def create_user_db(username, email, pwd):
    """
    Create a new user in the database.

    If the username is already taken, return True.
    """
    connection = get_db()
    # print("got here")
    # cur = connection.execute(
    #     "SELECT username "
    #     "FROM users "
    #     "WHERE username = ? ",
    #     (username, )
    # )
    # user = cur.fetchone()
    # if user:
    #     return True
    # connection.execute(
    #     "INSERT INTO users (username, email, password) "
    #     "VALUES (?, ?, ?)",
    #     (username, email, pwd)
    # )
    # return False
    try:
        connection.execute(
            "INSERT INTO users "
            "(username, email, password, status) "
            "VALUES (?, ?, ?, ?)",
            (username, email, pwd, 'none')
        )
        return False
    except:
        return True