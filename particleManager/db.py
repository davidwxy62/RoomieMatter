from particleManager.model import get_db, close_db
from particleManager.helper import check_password


def username_pwd_match_db(username, pwd):
    """
    Take in username and pw input from current user.

    If the password is right, login the user.
    """
    conn = get_db()
    cur = conn.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )

    user = cur.fetchone()
    close_db(conn)
    if not user:
        return False
    return check_password(user['password'], pwd)

def get_status_db(username):
    """Get the status of a user."""
    conn = get_db()

    cur = conn.execute(
        "SELECT status "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )

    user = cur.fetchone()
    close_db(conn)
    if not user:
        return None
    return user['status']


def change_status_db(username):
    """Change the status of a user."""
    conn = get_db()

    cur = conn.execute(
        "SELECT status "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )

    user = cur.fetchone()
    if not user:
        return None
    if user['status'] == 'active':
        conn.execute(
            "UPDATE users "
            "SET status = 'quiet' "
            "WHERE username = ?",
            (username, )
        )
    else:
        conn.execute(
            "UPDATE users "
            "SET status = 'active' "
            "WHERE username = ?",
            (username, )
        )
    close_db(conn)
    if user['status'] == 'active':
        return 'quiet'
    else:
        return 'active'


def username_hashed_pwd_match_db(username, hashed_pwd):
    """Check if a username and hashed password match."""
    conn = get_db()

    cur = conn.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    user = cur.fetchone()
    close_db(conn)
    if not user:
        return False
    return user['password'] == hashed_pwd