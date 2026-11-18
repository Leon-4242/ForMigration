from dataclasses import dataclass
from enum import StrEnum


class MessageTypes(StrEnum):
    COMMAND = "command"
    TEMPLATE = "template"


@dataclass(slots=True)
class Message:
    message_type: MessageTypes
    message_id: str
    text: str
