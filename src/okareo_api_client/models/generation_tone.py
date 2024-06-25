from enum import Enum


class GenerationTone(str, Enum):
    ABBREVIATED_INFORMAL = "Abbreviated Informal"
    EMPATHETIC = "Empathetic"
    FORMAL = "Formal"
    INFORMAL = "Informal"
    NEUTRAL = "Neutral"
    PERSUASIVE = "Persuasive"

    def __str__(self) -> str:
        return str(self.value)
