import logging
import sqlite3 as sq
from datetime import datetime

from modules.base.repository import ModuleRepository
from modules.consumer.config import CONSUMER_DB_PATH
from modules.consumer.types import BuildingType, ConsumerData, ConsumerInfoType, ConsumerRecord


class _Fields:
    building = "building"
    info_type = "info_type"
    place = "place"
    information = "information"


class _MetaFields:
    key = "key"
    value = "value"


_LAST_UPDATED_AT_KEY = "last_updated_at"


class ConsumerRepository(ModuleRepository):
    def __init__(self, filename=CONSUMER_DB_PATH) -> None:
        self.filename = filename
        self.con = sq.connect(filename)
        self.con.row_factory = sq.Row

        self.con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS consumer(
                id INTEGER PRIMARY KEY,
                {_Fields.building} TEXT NOT NULL,
                {_Fields.info_type} TEXT NOT NULL,
                {_Fields.place} TEXT NOT NULL,
                {_Fields.information} TEXT NOT NULL,
                UNIQUE(
                    {_Fields.building},
                    {_Fields.info_type},
                    {_Fields.place}
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

    def add(self, data: ConsumerData) -> None:
        self.con.execute(
            f"""
            INSERT INTO consumer (
                {_Fields.building},
                {_Fields.info_type},
                {_Fields.place},
                {_Fields.information}
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(
                {_Fields.building},
                {_Fields.info_type},
                {_Fields.place}
            )
            DO UPDATE SET
                {_Fields.information} = excluded.{_Fields.information}""",
            (data.building, data.info_type, data.place, data.text),
        )
        self.con.commit()

    def get(
        self,
        building: BuildingType,
        info_type: ConsumerInfoType,
        place: str,
    ) -> ConsumerRecord | None:
        row = self.con.execute(
            f"""
            SELECT * FROM consumer WHERE
                {_Fields.building} = ? AND
                {_Fields.info_type} = ? AND
                {_Fields.place} = ?""",
            (building, info_type, place),
        ).fetchone()
        if row is None:
            return None
        return ConsumerRecord.from_row(row)

    def get_buildings(self, info_type: ConsumerInfoType) -> list[BuildingType]:
        rows = self.con.execute(
            f"""
            SELECT DISTINCT {_Fields.building}
            FROM consumer
            WHERE {_Fields.info_type} = ?""",
            (info_type,),
        ).fetchall()
        buildings = [BuildingType(row[_Fields.building]) for row in rows]
        return sorted(buildings, key=lambda item: item.order)

    def get_places(
        self,
        building: BuildingType,
        info_type: ConsumerInfoType,
    ) -> list[str]:
        rows = self.con.execute(
            f"""
            SELECT {_Fields.place}
            FROM consumer
            WHERE {_Fields.building} = ? AND {_Fields.info_type} = ?
            ORDER BY {_Fields.place}""",
            (building, info_type),
        ).fetchall()
        return [row[_Fields.place] for row in rows]

    def get_single(
        self,
        building: BuildingType,
        info_type: ConsumerInfoType,
    ) -> ConsumerRecord | None:
        places = self.get_places(building, info_type)
        if not places:
            return None
        return self.get(building, info_type, places[0])

    def close(self) -> None:
        self.con.close()
