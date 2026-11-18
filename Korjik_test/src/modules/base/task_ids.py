from enum import StrEnum

from modules.base.types import ModuleId


class SystemTask(StrEnum):
    UPDATE_DATABASES = "update_databases"


def module_task_id(module: ModuleId) -> str:
    return f"module.{module.value}.update"
