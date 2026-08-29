from contextlib import contextmanager
import os
import sqlite3

DEFAULT_DB_PATH = os.path.realpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "DATA", "Bible.db")
)

@contextmanager
def get_db_cursor(db_path=None, factory=sqlite3.Row, connection=None):
    """Context manager for SQLite connections.

    Accepts a path, a string like ':memory:', or an existing connection object.
    """
    if connection:
        # Reuse an active connection (e.g. shared in-memory test DB)
        if factory:
            connection.row_factory = factory
        cur = connection.cursor()
        try:
            yield cur
            connection.commit()
        finally:
            cur.close()
        return

    path = db_path or DEFAULT_DB_PATH

    # Bypass file existence check for SQLite RAM databases
    if path != ":memory:" and not path.startswith("file:") and not os.path.exists(path):
        raise FileNotFoundError(f"Database file not found at: {path}")

    conn = sqlite3.connect(path)
    if factory:
        conn.row_factory = factory
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()
