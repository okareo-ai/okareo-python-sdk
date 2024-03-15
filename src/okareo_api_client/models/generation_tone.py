from enum import Enum


class GenerationTone(str, Enum):
    EMPATHETIC = "Empathetic"
    FORMAL = "Formal"
    INFORMAL = "Informal"
    NEUTRAL = "Neutral"
    PERSUASIVE = "Persuasive"

    def __str__(self) -> str:
        return str(self.value)
