"""roomieMatter development configuration."""
import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Secret key for encrypting cookies
SECRET_KEY = b'j\xa6\x04\xf7\xcf6\\Vdxhv\x07\xd7\xe5\xc8\xe4H\xb2s\x07\xa8I\x03'
SESSION_COOKIE_NAME = 'login'
# File Upload to var/uploads/
ROOMIEMATTER_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = ROOMIEMATTER_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
# Database file is var/roomieMatter.sqlite3
DATABASE_FILENAME = ROOMIEMATTER_ROOT/'var'/'roomieMatter.sqlite3'