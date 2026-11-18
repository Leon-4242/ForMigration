import logging
import sqlite3 as sq

from config.path import USERS_DIR
from models.user import User


class Fields:
    telegram_id = "id"
    name = "name"
    admin = "admin"


def from_row(row) -> User:
    return User(
        telegram_id=row[Fields.telegram_id], name=row[Fields.name], admin=bool(row[Fields.admin])
    )


class UsersDatabase:
    def __init__(self, filename=USERS_DIR):
        self.filename = filename
        self.con = sq.connect(filename)
        logging.info(f"Successfully Connected to {filename}:users")

        self.con.row_factory = sq.Row

        cursor = self.con.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS users(
            {Fields.telegram_id} INTEGER PRIMARY KEY,
            {Fields.name} TEXT,
            {Fields.admin} INTEGER DEFAULT 0
            )
        """
        )

    def get_by_name(self, name: str) -> User | None:
        data = self.con.execute(f"SELECT * FROM users WHERE {Fields.name} = ?", (name,)).fetchone()

        if data is None:
            return None

        return from_row(data)

    def get_by_id(self, telegram_id: int) -> User | None:
        data = self.con.execute(
            f"SELECT * FROM users WHERE {Fields.telegram_id} = ?", (telegram_id,)
        ).fetchone()

        if data is None:
            return None

        return from_row(data)

    def add_user(self, user: User) -> None:
        self.con.execute(
            f"INSERT INTO users ({Fields.telegram_id}, {Fields.name}, {Fields.admin}) VALUES (?, ?, ?)",
            (user.telegram_id, user.name, user.admin),
        )
        self.con.commit()

    def set_admin(self, telegram_id: int, admin: bool) -> None:
        self.con.execute(
            f"""UPDATE users SET {Fields.admin} = ? WHERE {Fields.telegram_id} = ?""",
            (admin, telegram_id),
        )

        self.con.commit()

    def get_users(self) -> list[User]:
        rows = self.con.execute("""SELECT * FROM users""").fetchall()

        return [from_row(row) for row in rows]

    def get_admins(self) -> list[User]:
        rows = self.con.execute(f"""SELECT * FROM users WHERE {Fields.admin} = 1""").fetchall()

        return [from_row(row) for row in rows]

    def close(self) -> None:
        self.con.close()
