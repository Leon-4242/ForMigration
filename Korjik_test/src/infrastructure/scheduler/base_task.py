from abc import ABC, abstractmethod

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class TaskGroup(ABC):
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        self.scheduler = scheduler

    @property
    @abstractmethod
    def task_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError
