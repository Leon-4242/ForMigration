import logging

from config.environment import BOT_TOKEN
from core.bot import TelegramBot
from core.filters.admin import AdminFilter
from core.lifecycle import BotLifecycle
from core.middlewares.registration import RegistrationMiddleware
from core.middlewares.service import ServiceMiddleware
from database.messages import MessagesDatabase
from database.users import UsersDatabase
from infrastructure.scheduler.main_scheduler import Scheduler
from infrastructure.scheduler.update_database import UpdateDatabaseTask
from infrastructure.services.bot_commands import BotCommandsService
from infrastructure.services.database import DatabaseService
from infrastructure.services.google_sheets import GoogleService
from infrastructure.services.messages import MessageService
from infrastructure.services.messenger import MessengerService
from infrastructure.services.users import UsersService
from system.admin.router import AdminRouter
from system.common.router import UserRouter
from system.echo.router import EchoRouter

from modules.base import BotModule
from modules.context import ModuleContext
from modules.registry import build_modules
from system.admin.commands import AdminBotCommands
from system.common.commands import CommonBotCommands


class Application:
    def __init__(self, token: str = BOT_TOKEN):
        self.bot = TelegramBot(token)
        self.lifecycle = BotLifecycle()
        self.restart_requested = False

    async def initialize(self) -> None:
        self.user_commands = list(CommonBotCommands)
        self.admin_commands = CommonBotCommands + AdminBotCommands
        self.modules: list[BotModule] = []

        self.initialize_databases()
        self.initialize_services()
        self.initialize_modules()

        self.initialize_middlewares()
        self.initialize_filters()

        self.initialize_routers()

        self.bot.setup_outer_middlewares(self.outer_middlewares)
        self.bot.setup_inner_middlewares(self.inner_middlewares)

        self.bot.include_routers(self.routers)
        await self.initialize_commands()
        self.initialize_scheduler()
        self.lifecycle.register(self.request_restart)

    def initialize_databases(self) -> None:
        self.users_database = UsersDatabase()
        self.messages_database = MessagesDatabase()

        self.databases = [
            self.users_database,
            self.messages_database,
        ]

    def initialize_services(self) -> None:
        self.users_service = UsersService(self.users_database)
        self.messages_service = MessageService(self.messages_database)
        self.google_service = GoogleService()
        self.messenger_service = MessengerService(bot=self.bot, users=self.users_service)
        self.database_service = DatabaseService(
            source=self.google_service, messages=self.messages_service
        )

        self.services = [
            self.users_service,
            self.messages_service,
            self.google_service,
            self.messenger_service,
            self.database_service,
        ]

    def initialize_modules(self) -> None:
        context = ModuleContext(
            google=self.google_service,
            messages=self.messages_service,
            users=self.users_service,
            messenger=self.messenger_service,
        )
        self.modules = build_modules(context)

        for module in self.modules:
            self.user_commands.extend(module.commands)
            self.admin_commands.extend(module.commands)

        self.bot_commands_service = BotCommandsService(
            user_commands=self.user_commands,
            admin_commands=self.admin_commands,
            bot=self.bot,
        )
        self.services.append(self.bot_commands_service)

    def initialize_scheduler(self) -> None:
        self.scheduler = Scheduler()

        self.scheduler.add_task(UpdateDatabaseTask, database_service=self.database_service)
        self.scheduler.add_module_tasks(self.modules)

    def initialize_middlewares(self) -> None:
        self.registration_middleware = RegistrationMiddleware(users=self.users_service)
        self.service_middleware = ServiceMiddleware(
            messenger=self.messenger_service,
            messages=self.messages_service,
            users=self.users_service,
            lifecycle=self.lifecycle,
            bot_commands=self.bot_commands_service,
        )

        self.outer_middlewares = [
            self.registration_middleware,
        ]

        self.inner_middlewares = [
            self.service_middleware,
        ]

    def initialize_filters(self) -> None:
        self.admin_filter = AdminFilter()

        self.filters = [
            self.admin_filter,
        ]

    def initialize_routers(self) -> None:
        self.user_router = UserRouter()
        self.admin_router = AdminRouter(admin_filter=self.admin_filter)
        self.echo_router = EchoRouter()

        self.routers = [
            self.user_router.get_router(),
            self.admin_router.get_router(),
            *[module.get_router() for module in self.modules],
            self.echo_router.get_router(),
        ]

    async def initialize_commands(self) -> None:
        await self.bot_commands_service.setup_all(users=self.users_service)

    async def startup(self):  # info about start bot
        logging.info("Bot has been started")
        self.database_service.update_databases()
        for module in self.modules:
            module.update()
        logging.info("Database has been updated")
        await self.messenger_service.broadcast_admin("Bot has been started")

    async def run(self) -> bool:
        """Запускает бота. В finally всегда вызывает shutdown. True — нужен перезапуск."""
        try:
            await self.scheduler.start()
            await self.bot.start(self.startup)
        finally:
            await self.shutdown()
        return self.restart_requested

    async def shutdown(self):
        logging.info("Bot has been stopped")
        await self.messenger_service.broadcast_admin("Bot has been stopped")
        await self.bot.stop_polling()
        await self.scheduler.shutdown()
        for module in self.modules:
            module.close()

        for service in self.services:
            service.close()

        for database in self.databases:
            database.close()

    async def request_restart(self) -> None:
        self.restart_requested = True
        await self.bot.stop_polling()
