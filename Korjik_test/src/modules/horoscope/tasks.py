from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.scheduler.base_task import TaskGroup
from modules.horoscope.repository import HoroscopeRepository
from modules.horoscope.service import HoroscopeService
from modules.horoscope.types import HoroscopeUser


class HoroscopeTaskGroup(TaskGroup):
    LOAD_JOB_ID = "module.horoscope.load"

    def __init__(
        self,
        scheduler: AsyncIOScheduler,
        service: HoroscopeService,
        repository: HoroscopeRepository,
    ) -> None:
        super().__init__(scheduler)
        self.service = service
        self.repository = repository

    @property
    def task_id(self) -> str:
        return "module.horoscope"

    @staticmethod
    def _user_job_id(telegram_id: int) -> str:
        return f"module.horoscope.user.{telegram_id}"

    async def start(self) -> None:
        self.scheduler.add_job(
            self.service.load_horoscopes,
            "cron",
            hour=0,
            minute=5,
            id=self.LOAD_JOB_ID,
        )

        for user in self.repository.get_all_users():
            await self.schedule_user(user)

    async def shutdown(self) -> None:
        for user in self.repository.get_all_users():
            job_id = self._user_job_id(user.telegram_id)
            if self.scheduler.get_job(job_id) is not None:
                self.scheduler.remove_job(job_id)

        if self.scheduler.get_job(self.LOAD_JOB_ID) is not None:
            self.scheduler.remove_job(self.LOAD_JOB_ID)

        await self.service.close()

    async def schedule_user(self, user: HoroscopeUser) -> None:
        self.scheduler.add_job(
            self.service.notify_user,
            "cron",
            hour=user.notify_time.hour,
            minute=user.notify_time.minute,
            kwargs={"user": user},
            id=self._user_job_id(user.telegram_id),
        )

    async def remove_user(self, user: HoroscopeUser) -> None:
        job_id = self._user_job_id(user.telegram_id)
        if self.scheduler.get_job(job_id) is not None:
            self.scheduler.remove_job(job_id)

    async def reschedule_user(self, user: HoroscopeUser) -> None:
        job_id = self._user_job_id(user.telegram_id)
        if self.scheduler.get_job(job_id) is None:
            await self.schedule_user(user)
            return

        self.scheduler.reschedule_job(
            job_id,
            trigger="cron",
            hour=user.notify_time.hour,
            minute=user.notify_time.minute,
        )
