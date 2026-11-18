from dataclasses import dataclass
from enum import StrEnum


class BuildingType(StrEnum):
    DS = "ДС"
    DSL = "ДСЛ"

    @property
    def order(self) -> int:
        return list(BuildingType).index(self)


class InfrastructureInfoType(StrEnum):
    ADMIN = "admin"
    INFO = "info"


class InfrastructureAction(StrEnum):
    ADMIN = "admin"


class InfrastructureStatus(StrEnum):
    CHOICE = "choice"
    READ = "read"


@dataclass(slots=True)
class InfrastructureData:
    building: BuildingType
    info_type: InfrastructureInfoType
    place: str
    text: str


@dataclass(slots=True)
class InfrastructureRecord:
    building: BuildingType
    info_type: InfrastructureInfoType
    place: str
    text: str

    @classmethod
    def from_row(cls, row) -> "InfrastructureRecord":
        return cls(
            building=BuildingType(row["building"]),
            info_type=InfrastructureInfoType(row["info_type"]),
            place=row["place"],
            text=row["information"],
        )
