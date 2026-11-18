from dataclasses import dataclass
from datetime import time
from enum import StrEnum


class HoroscopeSign(StrEnum):
    ARIES = "aries"
    TAURUS = "taurus"
    GEMINI = "gemini"
    CANCER = "cancer"
    LEO = "leo"
    VIRGO = "virgo"
    LIBRA = "libra"
    SCORPIO = "scorpio"
    SAGITTARIUS = "sagittarius"
    CAPRICORN = "capricorn"
    AQUARIUS = "aquarius"
    PISCES = "pisces"

    @property
    def symbol(self) -> str:
        return {
            HoroscopeSign.ARIES: "♈",
            HoroscopeSign.TAURUS: "♉",
            HoroscopeSign.GEMINI: "♊",
            HoroscopeSign.CANCER: "♋",
            HoroscopeSign.LEO: "♌",
            HoroscopeSign.VIRGO: "♍",
            HoroscopeSign.LIBRA: "♎",
            HoroscopeSign.SCORPIO: "♏",
            HoroscopeSign.SAGITTARIUS: "♐",
            HoroscopeSign.CAPRICORN: "♑",
            HoroscopeSign.AQUARIUS: "♒",
            HoroscopeSign.PISCES: "♓",
        }[self]


@dataclass(slots=True)
class HoroscopeUser:
    telegram_id: int
    telegram_name: str
    horoscope_sign: HoroscopeSign
    notify_time: time

    @classmethod
    def from_row(cls, row) -> "HoroscopeUser":
        return cls(
            telegram_id=row["telegram_id"],
            telegram_name=row["telegram_name"],
            horoscope_sign=HoroscopeSign(row["horoscope_sign"]),
            notify_time=time.fromisoformat(row["notify_time"]),
        )
