from database.messages import MessagesDatabase
from models.message import Message, MessageTypes


class MessageService:
    def __init__(self, messages: MessagesDatabase):
        self.messages = messages

    def add_message(self, message: Message) -> None:
        self.messages.add(message=message)

    def get_message(self, message_type: MessageTypes, message_id: str) -> Message | None:
        return self.messages.get(message_type=message_type, message_id=message_id)

    def get_text(self, message_type: MessageTypes, message_id: str) -> str | None:
        return self.messages.get_text(message_type=message_type, message_id=message_id)

    def update_message(self, message: Message) -> None:
        data = self.messages.get(message_type=message.message_type, message_id=message.message_id)
        if data is not None:
            self.messages.update(message=message)
        else:
            self.add_message(message=message)

    def close(self):
        pass
