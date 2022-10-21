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
    print(user)
    if not user:
        print(1)
        return None
    cur = connection.execute(
        "SELECT id "
        "FROM rooms "
        "WHERE roomname = ? ",
        (roomname, )
    )
    room = cur.fetchone()
    if not room:
        print(2)
        return None
    try:
        connection.execute(
            "INSERT INTO requests (roomId, senderId) "
            "VALUES (?, ?)",
            (room['id'], user['id'])
        )
        return room['id']
    except:
        print(3)
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
        "SELECT username, status "
        "FROM roomies INNER JOIN users "
        "ON roomies.roomieId = users.id "
        "WHERE roomId = ? AND username != ? ",
        (room['roomId'], username)
    )
    roomies = cur.fetchall()
    print(roomies)
    return roomies