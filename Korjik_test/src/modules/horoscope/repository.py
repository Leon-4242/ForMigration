import logging
import sqlite3 as sq

from modules.base.repository import ModuleRepository
from modules.horoscope.config import HOROSCOPE_DB_PATH
from modules.horoscope.types import HoroscopeSign, HoroscopeUser


class _Fields:
    telegram_id = "telegram_id"
    telegram_name = "telegram_name"
    horoscope_sign = "horoscope_sign"
    notify_time = "notify_time"


class HoroscopeRepository(ModuleRepository):
    def __init__(self, filename=HOROSCOPE_DB_PATH) -> None:
        self.filename = filename
        self.con = sq.connect(filename)
        self.con.row_factory = sq.Row

        self.con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS horoscope_users(
                {_Fields.telegram_id} INTEGER PRIMARY KEY,
                {_Fields.telegram_name} TEXT,
                {_Fields.horoscope_sign} TEXT,
                {_Fields.notify_time} TEXT
            )"""
        )
        self.con.commit()
        logging.info("Successfully connected to %s", filename)

    def is_subscribed(self, telegram_id: int) -> bool:
        row = self.con.execute(
            f"""
            SELECT EXISTS (
                SELECT 1 FROM horoscope_users
                WHERE {_Fields.telegram_id} = ?
            )""",
            (telegram_id,),
        ).fetchone()
        return bool(row[0])

    def get_all_users(self) -> list[HoroscopeUser]:
        rows = self.con.execute("SELECT * FROM horoscope_users").fetchall()
        return [HoroscopeUser.from_row(row) for row in rows]

    def get_user(self, telegram_id: int) -> HoroscopeUser | None:
        row = self.con.execute(
            f"SELECT * FROM horoscope_users WHERE {_Fields.telegram_id} = ?",
            (telegram_id,),
        ).fetchone()
        if row is None:
            return None
        return HoroscopeUser.from_row(row)

    def add_sub(
        self,
        telegram_id: int,
        username: str,
        sign: HoroscopeSign,
        hour: int,
        minute: int,
    ) -> None:
        self.con.execute(
            f"""
            INSERT INTO horoscope_users (
                {_Fields.telegram_id},
                {_Fields.telegram_name},
                {_Fields.horoscope_sign},
                {_Fields.notify_time}
            ) VALUES (?, ?, ?, ?)""",
            (telegram_id, username, sign.value, f"{hour:02d}:{minute:02d}"),
        )
        self.con.commit()

    def del_sub(self, telegram_id: int) -> None:
        self.con.execute(
            f"DELETE FROM horoscope_users WHERE {_Fields.telegram_id} = ?",
            (telegram_id,),
        )
        self.con.commit()

    def set_notify_time(self, telegram_id: int, hour: int, minute: int) -> None:
        self.con.execute(
            f"""
            UPDATE horoscope_users
            SET {_Fields.notify_time} = ?
            WHERE {_Fields.telegram_id} = ?""",
            (f"{hour:02d}:{minute:02d}", telegram_id),
        )
        self.con.commit()

    def close(self) -> None:
        self.con.close()
