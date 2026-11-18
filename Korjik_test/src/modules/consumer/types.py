from dataclasses import dataclass
from enum import StrEnum


class BuildingType(StrEnum):
    DS = "ДС"
    DSL = "ДСЛ"

    @property
    def order(self) -> int:
        return list(BuildingType).index(self)


class ConsumerInfoType(StrEnum):
    WASH = "wash"
    FOOD = "food"
    MARKET = "market"


class ConsumerAction(StrEnum):
    WASH = "wash"
    FOOD = "food"
    SHOP = "shop"
    BEDCLOTHES = "bedclothes"


class ConsumerStatus(StrEnum):
    CHOICE = "choice"
    READ = "read"


ACTION_TO_INFO_TYPE: dict[ConsumerAction, ConsumerInfoType] = {
    ConsumerAction.WASH: ConsumerInfoType.WASH,
    ConsumerAction.FOOD: ConsumerInfoType.FOOD,
    ConsumerAction.SHOP: ConsumerInfoType.MARKET,
    ConsumerAction.BEDCLOTHES: ConsumerInfoType.WASH,
}


@dataclass(slots=True)
class ConsumerData:
    building: BuildingType
    info_type: ConsumerInfoType
    place: str
    text: str


@dataclass(slots=True)
class ConsumerRecord:
    building: BuildingType
    info_type: ConsumerInfoType
    place: str
    text: str

    @classmethod
    def from_row(cls, row) -> "ConsumerRecord":
        return cls(
            building=BuildingType(row["building"]),
            info_type=ConsumerInfoType(row["info_type"]),
            place=row["place"],
            text=row["information"],
        )
