"""SQLite helpers for the StaffHub lab app."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def get_database_path() -> Path:
    """Return configured SQLite database path."""
    return Path(os.getenv("STAFFHUB_DB_PATH", "/app/data/staffhub.db"))


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row access by key."""
    db_path = get_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_database() -> None:
    """Create required schema if it does not already exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                department TEXT NOT NULL
            )
            """
        )
        conn.commit()
