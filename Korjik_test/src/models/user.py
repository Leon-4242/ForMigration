from dataclasses import dataclass


@dataclass(slots=True)
class User:
    telegram_id: int
    name: str
    admin: bool = False
