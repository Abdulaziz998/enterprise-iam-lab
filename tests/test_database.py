import sqlite3
from pathlib import Path

from app.database import Database


def test_database_file_created(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))

    db.initialize()

    assert db_file.exists()


def test_connect_and_close(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))

    conn = db.connect()
    assert isinstance(conn, sqlite3.Connection)
    assert db.connection is conn

    db.close()
    assert db.connection is None


def test_employees_table_exists(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))

    db.initialize()
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='employees';
        """
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "employees"
