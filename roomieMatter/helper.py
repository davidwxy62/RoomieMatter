"""Helper functions here and there."""
import hashlib
import os
import pathlib
import uuid
import roomieMatter
from roomieMatter import db

def loggedIn(cookie, auth_obj):
    """Help with both cookie and HTTP basic authorization."""
    print(cookie)
    if cookie:
        return True

    try:
        auth_user = auth_obj.get("username")
        auth_pwd = auth_obj.get("password")
    except AttributeError:
        return False

    if not auth_user or not auth_pwd:
        return False
    return db.username_pwd_match(auth_user, auth_pwd)