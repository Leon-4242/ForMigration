from collections.abc import Awaitable, Callable


class BotLifecycle:
    """Точка управления жизненным циклом бота для хендлеров без доступа к Application."""

    def __init__(self) -> None:
        self._restart: Callable[[], Awaitable[None]] | None = None

    def register(self, restart: Callable[[], Awaitable[None]]) -> None:
        self._restart = restart

    async def restart(self) -> None:
        if self._restart is None:
            raise RuntimeError("Restart handler is not registered")
        await self._restart()
