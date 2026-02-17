from enum import Enum


class UsagePrecision(str, Enum):
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    MONTH = "month"

    def __str__(self) -> str:
        return str(self.value)
