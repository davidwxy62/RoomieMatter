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

def create_user_db(username, name, email, pwd):
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
            "(username, name, email, password, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, name, email, pwd, 'active')
        )
        return False
    except:
        return True


def create_room_db(username, roomname):
    """Create a new room in the database."""
    connection = get_db()
    cur = connection.execute(
        "SELECT id "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return None
    try:
        connection.execute(
            "INSERT INTO rooms (roomname) VALUES (?)",
            (roomname, )
        )
        cur = connection.execute(
            "SELECT id "
            "FROM rooms "
            "WHERE roomname = ? ",
            (roomname, )
        )
        room = cur.fetchone()
        connection.execute(
            "INSERT INTO roomies (roomId, roomieId) "
            "VALUES (?, ?)",
            (room['id'], user['id'])
        )
        return room['id']
    except:
        return None


def request_db(username, roomname):
    """Request to join a room."""
    connection = get_db()
    cur = connection.execute(
        "SELECT id "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return None
    cur = connection.execute(
        "SELECT id "
        "FROM rooms "
        "WHERE roomname = ? ",
        (roomname, )
    )
    room = cur.fetchone()
    if not room:
        return None
    try:
        connection.execute(
            "INSERT INTO requests (roomId, senderId) "
            "VALUES (?, ?)",
            (room['id'], user['id'])
        )
        return room['id']
    except:
        return None


def get_roomies_db(username):
    """Get all roomies for a user."""
    connection = get_db()

    cur = connection.execute(
        "SELECT id "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return None
    
    cur = connection.execute(
        "SELECT roomId "
        "FROM roomies "
        "WHERE roomieId = ? ",
        (user['id'], )
    )
    room = cur.fetchone()
    if not room:
        return None

    cur = connection.execute(
        "SELECT name, status "
        "FROM roomies INNER JOIN users "
        "ON roomies.roomieId = users.id "
        "WHERE roomId = ? AND roomieId != ?",
        (room['roomId'], user['id'])
    )
    roomies = cur.fetchall()
    return roomies


def is_joined_db(username):
    """Check if a user is in a room."""
    connection = get_db()

    cur = connection.execute(
        "SELECT id "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return False
    
    cur = connection.execute(
        "SELECT roomId "
        "FROM roomies "
        "WHERE roomieId = ? ",
        (user['id'], )
    )
    room = cur.fetchone()
    if not room:
        return False
    return True


def get_name_db(username):
    """Get the name of a user."""
    connection = get_db()

    cur = connection.execute(
        "SELECT name "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return None
    return user['name']


def get_status_db(username):
    """Get the status of a user."""
    connection = get_db()

    cur = connection.execute(
        "SELECT status "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return None
    return user['status']


def change_status_db(username):
    """Change the status of a user."""
    connection = get_db()

    cur = connection.execute(
        "SELECT status "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return None
    if user['status'] == 'active':
        connection.execute(
            "UPDATE users "
            "SET status = 'quiet' "
            "WHERE username = ?",
            (username, )
        )
    else:
        connection.execute(
            "UPDATE users "
            "SET status = 'active' "
            "WHERE username = ?",
            (username, )
        )
    if user['status'] == 'active':
        return 'quiet'
    else:
        return 'active'