from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.scheduler.base_task import TaskGroup
from infrastructure.services.database import DatabaseService
from modules.base.task_ids import SystemTask


class UpdateDatabaseTask(TaskGroup):
    def __init__(self, database_service: DatabaseService, scheduler: AsyncIOScheduler):
        self.database_service = database_service
        super().__init__(scheduler)

    @property
    def task_id(self) -> str:
        return SystemTask.UPDATE_DATABASES.value

    async def start(self) -> None:
        self.scheduler.add_job(
            self._update_databases,
            id=self.task_id,
            trigger="interval",
            hours=1,
        )

    async def _update_databases(self) -> None:
        self.database_service.update_databases()

    async def shutdown(self) -> None:
        self.scheduler.remove_job(self.task_id)
