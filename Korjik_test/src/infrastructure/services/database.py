import logging

from infrastructure.services.google_sheets import GoogleService
from infrastructure.services.messages import MessageService
from models.message import Message, MessageTypes
from models.sheet_types import SheetTypes


class DatabaseService:
    def __init__(self, source: GoogleService, messages: MessageService):
        self.source = source
        self.messages = messages

    def update_databases(self):
        logging.info("Updating databases")
        self.update_messages()

    def update_messages(self):
        data = self.source.get_from_table(SheetTypes.MESSAGES)
        for item in data:
            self.messages.update_message(
                Message(
                    message_type=MessageTypes(item["message_type"]),
                    message_id=item["message_id"],
                    text=item["text"],
                )
            )

    def close(self):
        pass
