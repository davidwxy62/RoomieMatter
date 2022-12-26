"""Helpers related to sql querying."""
import flask
from roomieMatter.model import get_db
from roomieMatter import helper

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
    return helper.check_password(user['password'], pwd)


def create_user_db(username, name, email, pwd):
    """
    Create a new user in the database.

    If the username is already taken, return True.
    """
    connection = get_db()
    email = email.lower()


    try:
        connection.execute(
            "INSERT INTO users "
            "(username, name, email, password, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, name, email, helper.hash_password(pwd), 'active')
        )
        return False
    except:
        cur = connection.execute(
            "SELECT * "
            "FROM users "
            "WHERE username = ?",
            (username, )
        )
        if cur.fetchone():
            return "Username already taken"
        cur = connection.execute(
            "SELECT * "
            "FROM users "
            "WHERE email = ?",
            (email, )
        )
        if cur.fetchone():
            return "Email already taken"
        return True # Unknown error


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
    roomies.sort(key=lambda x: x['name'])
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
    print(username)
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


def has_pending_requests_db(username):
    """Check if a user has pending requests."""
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

    cur = connection.execute(
        "SELECT senderId "
        "FROM requests "
        "WHERE roomId = ? ",
        (room['roomId'], )
    )
    request = cur.fetchone()
    if not request:
        return False
    return True


def delete_pending_requests_db(username, sender_id):
    """Delete a pending request."""
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

    try:
        connection.execute(
            "DELETE FROM requests "
            "WHERE roomId = ? AND senderId = ?",
            (room['roomId'], sender_id)
        )
        return True
    except:
        return False


def get_pending_requests_db(username):
    """Get all pending requests."""
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
        "SELECT name, senderId "
        "FROM requests INNER JOIN users "
        "ON requests.senderId = users.id "
        "WHERE roomId = ?",
        (room['roomId'], )
    )
    requests = cur.fetchall()
    return requests


def add_roomie_db(username, sender_id):
    """Add a roomie to a room."""
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

    try:
        connection.execute(
            "INSERT INTO roomies (roomId, roomieId) "
            "VALUES (?, ?)",
            (room['roomId'], sender_id)
        )
        return True
    except:
        return False


def get_roomname_db(username):
    """Get the room of a user."""
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
        "SELECT roomname "
        "FROM rooms "
        "WHERE id = ?",
        (room['roomId'], )
    )
    roomname = cur.fetchone()
    if not roomname:
        return None

    return roomname['roomname']


def get_all_info_db(username):
    """Get name, email, and room of a user."""
    connection = get_db()

    cur = connection.execute(
        "SELECT id, name, email "
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
        return user['name'], user['email'], ""

    cur = connection.execute(
        "SELECT roomname "
        "FROM rooms "
        "WHERE id = ?",
        (room['roomId'], )
    )
    roomname = cur.fetchone()
    if not roomname:
        return None

    return user['name'], user['email'], roomname['roomname']


def change_username_db(username, new_username):
    """Change a user's username."""
    connection = get_db()

    try:
        connection.execute(
            "UPDATE users "
            "SET username = ? "
            "WHERE username = ?",
            (new_username, username)
        )
        return None
    except:
        return "Username already taken"


def change_name_db(username, new_name):
    """Change a user's name."""
    connection = get_db()

    # return error if roomie has the same name in the same room
    cur = connection.execute(
        "SELECT roomId "
        "FROM roomies INNER JOIN users "
        "ON roomies.roomieId = users.id "
        "WHERE users.username = ?",
        (username, )
    )
    room = cur.fetchone()
    if not room:
        return "Unknown error"

    cur = connection.execute(
        "SELECT name "
        "FROM roomies INNER JOIN users "
        "ON roomies.roomieId = users.id "
        "WHERE roomies.roomId = ?",
        (room['roomId'], )
    )
    roomies = cur.fetchall()

    if new_name in [roomie['name'] for roomie in roomies]:
        return "Name already taken"

    try:
        connection.execute(
            "UPDATE users "
            "SET name = ? "
            "WHERE username = ?",
            (new_name, username)
        )
        return None
    except:
        return "Unknown error"


def change_email_db(username, new_email):
    """Change a user's email."""
    connection = get_db()
    new_email = new_email.lower()

    try:
        connection.execute(
            "UPDATE users "
            "SET email = ? "
            "WHERE username = ?",
            (new_email, username)
        )
        return None
    except:
        return "Email already taken"


def change_roomname_db(username, new_room_name):
    """Change a user's room name."""
    connection = get_db()

    cur = connection.execute(
        "SELECT id "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return "Unknown error"
    
    cur = connection.execute(
        "SELECT roomId "
        "FROM roomies "
        "WHERE roomieId = ? ",
        (user['id'], )
    )
    room = cur.fetchone()
    if not room:
        return "Unknown error"

    try:
        connection.execute(
            "UPDATE rooms "
            "SET roomname = ? "
            "WHERE id = ?",
            (new_room_name, room['roomId'])
        )
        return None
    except:
        return "Room name already taken"


def exit_room_db(username):
    """Remove a user from their room."""
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

    try:
        connection.execute(
            "DELETE FROM roomies "
            "WHERE roomId = ? AND roomieId = ?",
            (room['roomId'], user['id'])
        )
        delete_empty_rooms_db()
        return True
    except:
        return False


def delete_empty_rooms_db():
    """Delete all empty rooms."""
    connection = get_db()

    try:
        connection.execute(
            "DELETE FROM rooms "
            "WHERE id NOT IN (SELECT roomId FROM roomies)"
        )
        return True
    except:
        return False


def update_ip_db(args):
    """Update a user's IP."""
    connection = get_db()

    try:
        connection.execute(
            "UPDATE users "
            "SET IP = ? "
            "WHERE username = ?",
            (args['IP'], args['username'])
        )
        return True
    except:
        return False


def change_profile_db(form, username):
    """Change a user's profile."""
    connection = get_db()

    # changing username
    try:
        connection.execute(
            "UPDATE users "
            "SET username = ? "
            "WHERE username = ?",
            (form['username'], username)
        )
    except:
        return "Username already taken"
    username = form['username']
    flask.session['username'] = username
    
    # changing name
    # return error if roomie has the same name in the same room
    cur = connection.execute(
        "SELECT roomId "
        "FROM roomies INNER JOIN users "
        "ON roomies.roomieId = users.id "
        "WHERE users.username = ?",
        (username, )
    )
    room = cur.fetchone()
    if not room:
        return "Unknown error"
    cur = connection.execute(
        "SELECT name "
        "FROM roomies INNER JOIN users "
        "ON roomies.roomieId = users.id "
        "WHERE roomies.roomId = ? AND users.username != ?",
        (room['roomId'], username)
    )
    roomies = cur.fetchall()
    if form['name'] in [roomie['name'] for roomie in roomies]:
        return "Name already taken"
    try:
        connection.execute(
            "UPDATE users "
            "SET name = ? "
            "WHERE username = ?",
            (form['name'], username)
        )
    except:
        return "Unknown error"

    # changing email
    new_email = form['email'].lower()
    try:
        connection.execute(
            "UPDATE users "
            "SET email = ? "
            "WHERE username = ?",
            (new_email, username)
        )
    except:
        return "Email already taken"

    # changing room name
    cur = connection.execute(
        "SELECT id "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    user = cur.fetchone()
    if not user:
        return "Unknown error"
    cur = connection.execute(
        "SELECT roomId "
        "FROM roomies "
        "WHERE roomieId = ? ",
        (user['id'], )
    )
    room = cur.fetchone()
    if not room:
        return "Unknown error"
    try:
        connection.execute(
            "UPDATE rooms "
            "SET roomname = ? "
            "WHERE id = ?",
            (form['room'], room['roomId'])
        )
    except:
        return "Room name already taken"
    return None

