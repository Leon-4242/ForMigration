from abc import ABC, abstractmethod


class ModuleRepository(ABC):
    """Хранилище модуля. Конкретные репозитории добавляют свои методы чтения/записи."""

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
