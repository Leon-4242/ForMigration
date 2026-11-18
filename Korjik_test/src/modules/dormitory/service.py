from collections.abc import Iterable
from datetime import datetime

from infrastructure.services.google_sheets import GoogleService
from infrastructure.services.messages import MessageService
from models.message import MessageTypes
from modules.base.sync import SheetSyncService
from modules.dormitory.repository import DormitoryRepository
from modules.dormitory.types import BuildingType, CorpusType, DormitoryData, InfoType
from modules.types import Modules, sheets_for_module


class DormitoryService:
    _TEMPLATE_COMENDA = "comenda"
    _TEMPLATE_CHECK_ROOM = "check_room"
    _TEMPLATE_STAROSTA = "starosta"

    def __init__(
        self,
        repository: DormitoryRepository,
        source: GoogleService,
        messages: MessageService,
    ) -> None:
        self.repository = repository
        self.source = source
        self.messages = messages

    def update(self) -> None:
        self.repository.set_last_updated_at(datetime.now())
        SheetSyncService(
            source=self.source,
            sheets=sheets_for_module(Modules.DORMITORY),
            parser=self.parse_row,
            sink=self.repository.add,
        ).update()

    def parse_row(self, row: dict) -> Iterable[DormitoryData]:
        last_data_update = self.repository.format_last_updated_at()
        building = BuildingType(row["building"])
        corpus = CorpusType(row["corpus"])
        floor_start = int(row["floor_start"])
        floor_end = int(row["floor_end"])

        for floor in range(floor_start, floor_end + 1):
            yield self._build_comenda(row, building, corpus, floor, last_data_update)
            yield self._build_roomcheck(row, building, corpus, floor, last_data_update)
            yield self._build_starosta(row, building, corpus, floor, last_data_update)

    def _format_template(self, template_id: str, **kwargs: str) -> str:
        template = self.messages.get_text(MessageTypes.TEMPLATE, template_id)
        if template is None:
            return ""
        return template.format(**kwargs)

    def _build_comenda(
        self,
        row: dict,
        building: BuildingType,
        corpus: CorpusType,
        floor: int,
        last_data_update: str,
    ) -> DormitoryData:
        text = self._format_template(
            self._TEMPLATE_COMENDA,
            comenda_name=row["comenda"],
            comenda_room=row["comenda_room"],
            comenda_work_time=row.get("comenda_work_time", ""),
            dezhurnii_phone=row.get("dezhurnu_phone", ""),
            dezhurnii_room=row["dezhurnu_room"],
            last_data_update=last_data_update,
        )
        return DormitoryData(
            building=building,
            corpus=corpus,
            floor=floor,
            info_type=InfoType.COMENDA,
            text=text,
        )

    def _build_roomcheck(
        self,
        row: dict,
        building: BuildingType,
        corpus: CorpusType,
        floor: int,
        last_data_update: str,
    ) -> DormitoryData:
        text = self._format_template(
            self._TEMPLATE_CHECK_ROOM,
            check_rooms_range_time=row["room_check_range_time"],
            last_data_update=last_data_update,
        )
        return DormitoryData(
            building=building,
            corpus=corpus,
            floor=floor,
            info_type=InfoType.ROOMCHECK,
            text=text,
        )

    def _build_starosta(
        self,
        row: dict,
        building: BuildingType,
        corpus: CorpusType,
        floor: int,
        last_data_update: str,
    ) -> DormitoryData:
        text = self._format_template(
            self._TEMPLATE_STAROSTA,
            starosta_1=row.get("starosta_1", ""),
            link_1=row.get("starosta_1_link", ""),
            starosta_2=row.get("starosta_2", ""),
            link_2=row.get("starosta_2_link", ""),
            starosta_3=row.get("starosta_3", ""),
            link_3=row.get("starosta_3_link", ""),
            last_data_update=last_data_update,
        )
        return DormitoryData(
            building=building,
            corpus=corpus,
            floor=floor,
            info_type=InfoType.STAROSTA,
            text=text,
        )
