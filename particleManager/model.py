"""roomieMatter model (database) API."""
import sqlite3
from particleManager import config


def dict_factory(cursor, row):
    """
    Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """
    Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    db_filename = config.DATABASE_FILENAME
    conn = sqlite3.connect(str(db_filename))
    conn.row_factory = dict_factory
    # Foreign keys have to be enabled per-connection.  This is an sqlite3
    # backwards compatibility thing.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def close_db(conn):
    """
    Close the database at the end of a request.
    """
    conn.commit()
    conn.close()
