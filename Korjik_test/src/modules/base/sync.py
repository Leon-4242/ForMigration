from collections.abc import Callable, Iterable
from typing import TypeVar

from infrastructure.services.google_sheets import GoogleService
from models.sheet_types import SheetTypes

T = TypeVar("T")


class SheetSyncService:
    """Общий сценарий синхронизации Google Sheets → sink (обычно SQLite-репозиторий)."""

    def __init__(
        self,
        source: GoogleService,
        sheets: list[SheetTypes],
        parser: Callable[[dict], Iterable[T]],
        sink: Callable[[T], None],
    ) -> None:
        self.source = source
        self.sheets = sheets
        self.parser = parser
        self.sink = sink

    def update(self) -> None:
        for sheet in self.sheets:
            for row in self.source.get_from_table(sheet):
                for item in self.parser(row):
                    self.sink(item)
