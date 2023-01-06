"""Helper functions here and there."""
import hashlib
import uuid

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
