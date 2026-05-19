from enum import Enum


class PanelConfigChartType(str, Enum):
    AREA = "area"
    BAR = "bar"
    COMPOSED = "composed"
    LINE = "line"
    RADAR = "radar"
    STAT = "stat"
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)
