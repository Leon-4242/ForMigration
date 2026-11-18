from datetime import datetime

from infrastructure.services.google_sheets import GoogleService
from models.sheet_types import SheetTypes
from modules.consumer.repository import ConsumerRepository
from modules.consumer.types import BuildingType, ConsumerData, ConsumerInfoType
from modules.types import Modules, sheets_for_module

_SHEET_INFO_TYPES: dict[SheetTypes, ConsumerInfoType] = {
    SheetTypes.FOOD: ConsumerInfoType.FOOD,
    SheetTypes.SHOP: ConsumerInfoType.MARKET,
    SheetTypes.WASH: ConsumerInfoType.WASH,
}


class ConsumerService:
    def __init__(
        self,
        repository: ConsumerRepository,
        source: GoogleService,
    ) -> None:
        self.repository = repository
        self.source = source

    def update(self) -> None:
        self.repository.set_last_updated_at(datetime.now())

        for sheet in sheets_for_module(Modules.CONSUMER):
            info_type = _SHEET_INFO_TYPES[sheet]
            for row in self.source.get_from_table(sheet):
                self.repository.add(self.parse_row(row, info_type))

    def parse_row(self, row: dict, info_type: ConsumerInfoType) -> ConsumerData:
        building = BuildingType(row["building"])
        place = str(row.get("place") or row.get("name") or building.value)
        text = str(row.get("information") or row.get("text") or "")
        last_data_update = self.repository.format_last_updated_at()
        if "{last_data_update}" in text:
            text = text.format(last_data_update=last_data_update)
        return ConsumerData(
            building=building,
            info_type=info_type,
            place=place,
            text=text,
        )
