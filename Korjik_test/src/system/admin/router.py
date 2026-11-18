from aiogram import F, Router
from aiogram.filters import Command, StateFilter

from core.filters.admin import AdminFilter
from system.admin.commands import AdminCommands
from system.admin.handlers import command_admin_help, command_restart, command_set_admin
from system.admin.keyboard import NotifyCallback
from system.admin.notify import Notify, cancel_notify, command_notify, forming_notify, send_notify


class AdminRouter:
    def __init__(self, admin_filter: AdminFilter):
        self.router = Router()

        self.router.message.filter(admin_filter)
        self.router.callback_query.filter(admin_filter)

        self.router.message.register(command_restart, Command(AdminCommands.RESTART))
        self.router.message.register(command_admin_help, Command(AdminCommands.ADMIN_HELP))
        self.router.message.register(command_set_admin, Command(AdminCommands.SET_ADMIN))

        self.router.message.register(command_notify, Command(AdminCommands.NOTIFY))
        self.router.message.register(forming_notify, StateFilter(Notify.notify))
        self.router.callback_query.register(send_notify, NotifyCallback.filter(F.send))
        self.router.callback_query.register(cancel_notify, NotifyCallback.filter(~F.send))

    def get_router(self) -> Router:
        return self.router
