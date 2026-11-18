from dataclasses import dataclass

from infrastructure.services.google_sheets import GoogleService
from infrastructure.services.messages import MessageService
from infrastructure.services.messenger import MessengerService
from infrastructure.services.users import UsersService


@dataclass(frozen=True, slots=True)
class ModuleContext:
    """
    Зависимости, доступные feature-модулям при сборке.

    Модули не импортируют Application — только этот контекст и абстракции из modules.base.
    """

    google: GoogleService
    messages: MessageService
    users: UsersService
    messenger: MessengerService
