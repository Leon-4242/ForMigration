from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


class BuildingType(StrEnum):
    DS = "ДС"
    DSL = "ДСЛ"

    @property
    def order(self) -> int:
        return list(BuildingType).index(self)


class CorpusType(StrEnum):
    A = "А"
    B = "Б"
    V = "В"
    G = "Г"
    D = "Д"
    E = "Е"
    ZGE = "Ж"

    @property
    def order(self) -> int:
        return list(CorpusType).index(self)


class InfoType(StrEnum):
    COMENDA = "comenda"
    ROOMCHECK = "roomcheck"
    STAROSTA = "starosta"


FloorLimit = Literal[
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
]


@dataclass(slots=True)
class DormitoryData:
    building: BuildingType
    corpus: CorpusType
    floor: int
    info_type: InfoType
    text: str


@dataclass(slots=True)
class DormitoryRecord:
    building: BuildingType
    corpus: CorpusType
    floor: int
    info_type: InfoType
    text: str

    @classmethod
    def from_row(cls, row) -> "DormitoryRecord":
        return cls(
            building=BuildingType(row["building"]),
            corpus=CorpusType(row["corpus"]),
            floor=int(row["floor"]),
            info_type=InfoType(row["info_type"]),
            text=row["information"],
        )
