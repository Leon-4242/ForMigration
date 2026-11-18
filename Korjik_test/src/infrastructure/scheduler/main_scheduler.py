from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.scheduler.base_task import TaskGroup
from modules.base.module import BotModule


class Scheduler:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.tasks: dict[str, TaskGroup] = {}

    def add_task(self, task_cls: type[TaskGroup], **kwargs) -> None:
        task = task_cls(scheduler=self.scheduler, **kwargs)
        self.tasks[task.task_id] = task

    def add_module_tasks(self, modules: list[BotModule], **kwargs) -> None:
        for module in modules:
            task = module.build_tasks(self.scheduler, **kwargs)
            self.tasks[task.task_id] = task

    async def start(self) -> None:
        for task_group in self.tasks.values():
            await task_group.start()

        self.scheduler.start()

    async def shutdown(self) -> None:
        for task_group in self.tasks.values():
            await task_group.shutdown()
        self.scheduler.shutdown()
