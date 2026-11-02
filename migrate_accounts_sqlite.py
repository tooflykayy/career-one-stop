import sqlite3
from pathlib import Path


def migrate():
    database = Path(__file__).parent / "instance" / "career_one_stop.db"

    if not database.is_file():
        raise SystemExit("Database not found. No changes made.")

    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        tables = ("skill", "application", "learning_activity")

        for table in tables:
            columns = connection.execute(
                f'PRAGMA table_info("{table}")'
            ).fetchall()
            if not columns:
                raise SystemExit(f"Missing table: {table}. No changes made.")

        connection.execute("BEGIN")
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                email VARCHAR(254) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            )
        """)

        for table in tables:
            columns = {
                row[1]
                for row in connection.execute(
                    f'PRAGMA table_info("{table}")'
                )
            }

            if "user_id" not in columns:
                connection.execute(
                    f'ALTER TABLE "{table}" '
                    'ADD COLUMN user_id INTEGER REFERENCES user(id)'
                )

            connection.execute(
                f'CREATE INDEX IF NOT EXISTS "ix_{table}_user_id" '
                f'ON "{table}" (user_id)'
            )

    print("Account tables updated. Existing records preserved.")


if __name__ == "__main__":
    migrate()