from enum import Enum


class TimeRange(str, Enum):
    LAST_14_DAYS = "LAST_14_DAYS"
    LAST_24_HOURS = "LAST_24_HOURS"
    LAST_30_DAYS = "LAST_30_DAYS"
    LAST_7_DAYS = "LAST_7_DAYS"
    LAST_90_DAYS = "LAST_90_DAYS"
    LAST_HOUR = "LAST_HOUR"

    def __str__(self) -> str:
        return str(self.value)
