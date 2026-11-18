import logging
import sqlite3 as sq
from datetime import datetime

from modules.base.repository import ModuleRepository
from modules.dormitory.config import DORMITORY_DB_PATH
from modules.dormitory.types import (
    BuildingType,
    CorpusType,
    DormitoryData,
    DormitoryRecord,
    InfoType,
)


class _Fields:
    building = "building"
    corpus = "corpus"
    floor = "floor"
    info_type = "info_type"
    information = "information"


class _MetaFields:
    key = "key"
    value = "value"


_LAST_UPDATED_AT_KEY = "last_updated_at"

class DormitoryRepository(ModuleRepository):
    def __init__(self, filename=DORMITORY_DB_PATH) -> None:
        self.filename = filename
        self.con = sq.connect(filename)
        self.con.row_factory = sq.Row

        self.con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS dormitory(
                id INTEGER PRIMARY KEY,
                {_Fields.building} TEXT NOT NULL,
                {_Fields.corpus} TEXT NOT NULL,
                {_Fields.floor} INTEGER NOT NULL,
                {_Fields.info_type} TEXT NOT NULL,
                {_Fields.information} TEXT NOT NULL,
                UNIQUE(
                    {_Fields.building},
                    {_Fields.corpus},
                    {_Fields.floor},
                    {_Fields.info_type}
                )
            )"""
        )
        self.con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS meta(
                {_MetaFields.key} TEXT PRIMARY KEY,
                {_MetaFields.value} TEXT NOT NULL
            )"""
        )
        self.con.commit()
        logging.info("Successfully connected to %s", filename)

    def set_last_updated_at(self, moment: datetime) -> None:
        self.con.execute(
            f"""
            INSERT INTO meta ({_MetaFields.key}, {_MetaFields.value})
            VALUES (?, ?)
            ON CONFLICT({_MetaFields.key})
            DO UPDATE SET {_MetaFields.value} = excluded.{_MetaFields.value}""",
            (_LAST_UPDATED_AT_KEY, moment.isoformat()),
        )
        self.con.commit()

    def get_last_updated_at(self) -> datetime | None:
        row = self.con.execute(
            f"SELECT {_MetaFields.value} FROM meta WHERE {_MetaFields.key} = ?",
            (_LAST_UPDATED_AT_KEY,),
        ).fetchone()
        if row is None:
            return None
        return datetime.fromisoformat(row[_MetaFields.value])

    def format_last_updated_at(self) -> str:
        moment = self.get_last_updated_at()
        if moment is None:
            return ""
        return moment.strftime("%d.%m.%Y %H:%M")
    def add(self, data: DormitoryData) -> None:
        self.con.execute(
            f"""
            INSERT INTO dormitory (
                {_Fields.building},
                {_Fields.corpus},
                {_Fields.floor},
                {_Fields.info_type},
                {_Fields.information}
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(
                {_Fields.building},
                {_Fields.corpus},
                {_Fields.floor},
                {_Fields.info_type}
            )
            DO UPDATE SET
                {_Fields.information} = excluded.{_Fields.information}""",
            (data.building, data.corpus, data.floor, data.info_type, data.text),
        )
        self.con.commit()

    def get(
        self,
        building: BuildingType,
        corpus: CorpusType,
        floor: int,
        info_type: InfoType,
    ) -> DormitoryRecord | None:
        row = self.con.execute(
            f"""
            SELECT * FROM dormitory WHERE
                {_Fields.building} = ? AND
                {_Fields.corpus} = ? AND
                {_Fields.floor} = ? AND
                {_Fields.info_type} = ?""",
            (building, corpus, floor, info_type),
        ).fetchone()

        if row is None:
            return None

        return DormitoryRecord.from_row(row)

    def get_buildings(self) -> list[BuildingType]:
        rows = self.con.execute(
            f"SELECT DISTINCT {_Fields.building} FROM dormitory"
        ).fetchall()
        buildings = [BuildingType(row[_Fields.building]) for row in rows]
        return sorted(buildings, key=lambda item: item.order)

    def get_corpuses(self, building: BuildingType) -> list[CorpusType]:
        rows = self.con.execute(
            f"""
            SELECT DISTINCT {_Fields.corpus}
            FROM dormitory
            WHERE {_Fields.building} = ?""",
            (building,),
        ).fetchall()
        corpuses = [CorpusType(row[_Fields.corpus]) for row in rows]
        return sorted(corpuses, key=lambda item: item.order)

    def get_floors(self, building: BuildingType, corpus: CorpusType) -> list[int]:
        rows = self.con.execute(
            f"""
            SELECT DISTINCT {_Fields.floor}
            FROM dormitory
            WHERE {_Fields.building} = ? AND {_Fields.corpus} = ?
            ORDER BY {_Fields.floor}""",
            (building, corpus),
        ).fetchall()
        return [int(row[_Fields.floor]) for row in rows]

    def close(self) -> None:
        self.con.close()
