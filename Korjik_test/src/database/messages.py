import logging
import sqlite3 as sq

from config.path import MESSAGES_DIR
from models.message import Message, MessageTypes


class Fields:
    message_type = "message_type"
    message_id = "message_id"
    text = "text"


def from_row(row: dict) -> Message:
    return Message(
        message_type=MessageTypes(row[Fields.message_type]),
        message_id=row[Fields.message_id],
        text=row[Fields.text],
    )


class MessagesDatabase:
    def __init__(self, filename=MESSAGES_DIR):
        self.filename = filename
        self.con = sq.connect(filename)
        logging.info(f"Successfully Connected to {filename}:messages")

        self.con.row_factory = sq.Row

        self.con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS messages(
            {Fields.message_type} TEXT NOT NULL,
            {Fields.message_id} TEXT NOT NULL,
            {Fields.text} TEXT,
            UNIQUE({Fields.message_type}, {Fields.message_id})
            )
        """
        )
        self.con.commit()

    def add(self, message: Message) -> None:
        self.con.execute(
            f"""INSERT INTO messages
                            ({Fields.message_type}, {Fields.message_id}, {Fields.text})
                            VALUES (?, ?, ?)
                         """,
            (message.message_type, message.message_id, message.text),
        )

        self.con.commit()

    def update(self, message: Message) -> None:
        self.con.execute(
            f"""UPDATE messages
                            SET {Fields.text} = ?
                            WHERE {Fields.message_type} = ? and {Fields.message_id} = ?""",
            (message.text, message.message_type, message.message_id),
        )
        self.con.commit()

    def get_text(self, message_type: MessageTypes, message_id: str) -> str | None:
        data = self.con.execute(
            f"""SELECT {Fields.text} FROM messages
                                WHERE {Fields.message_type} = ? and {Fields.message_id} = ?""",
            (message_type, message_id),
        ).fetchone()
        if data is None:
            return None

        return data[Fields.text]

    def get(self, message_type: MessageTypes, message_id: str) -> Message | None:
        data = self.con.execute(
            f"""SELECT * FROM messages
                                WHERE {Fields.message_type} = ? and {Fields.message_id} = ?""",
            (message_type, message_id),
        ).fetchone()
        if data is None:
            return None

        return from_row(data)

    def close(self) -> None:
        self.con.close()