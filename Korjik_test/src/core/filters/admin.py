from aiogram.filters import Filter

from models.user import User


class AdminFilter(Filter):
    async def __call__(self, event, user: User) -> bool:
        return user.admin
