from enum import Enum


class PanelTableConfigMode(str, Enum):
    FLAT = "flat"
    PIVOT = "pivot"

    def __str__(self) -> str:
        return str(self.value)
