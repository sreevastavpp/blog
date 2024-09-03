import sqlite3


class UserDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_user(self, username, email):
        self.cursor.execute(
            """
            INSERT INTO users (username, email) VALUES (?, ?)
        """,
            (username, email),
        )
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
