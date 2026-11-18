from datetime import datetime

from infrastructure.services.google_sheets import GoogleService
from models.sheet_types import SheetTypes
from modules.infrastructure.repository import InfrastructureRepository
from modules.infrastructure.types import BuildingType, InfrastructureData, InfrastructureInfoType
from modules.types import Modules, sheets_for_module

_SHEET_INFO_TYPES: dict[SheetTypes, InfrastructureInfoType] = {
    SheetTypes.ADMIN: InfrastructureInfoType.ADMIN,
    SheetTypes.INFO: InfrastructureInfoType.INFO,
}


class InfrastructureService:
    def __init__(
        self,
        repository: InfrastructureRepository,
        source: GoogleService,
    ) -> None:
        self.repository = repository
        self.source = source

    def update(self) -> None:
        self.repository.set_last_updated_at(datetime.now())

        for sheet in sheets_for_module(Modules.INFRASTRUCTURE):
            info_type = _SHEET_INFO_TYPES[sheet]
            for row in self.source.get_from_table(sheet):
                self.repository.add(self.parse_row(row, info_type))

    def parse_row(self, row: dict, info_type: InfrastructureInfoType) -> InfrastructureData:
        building = BuildingType(row["building"])
        place = str(row.get("place") or building.value)
        text = str(row.get("information") or "")
        last_data_update = self.repository.format_last_updated_at()
        if "{last_data_update}" in text:
            text = text.format(last_data_update=last_data_update)
        return InfrastructureData(
            building=building,
            info_type=info_type,
            place=place,
            text=text,
        )
