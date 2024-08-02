from enum import Enum


class TestRunType(str, Enum):
    INFORMATION_RETRIEVAL = "INFORMATION_RETRIEVAL"
    INVARIANT = "invariant"
    MULTI_CLASS_CLASSIFICATION = "MULTI_CLASS_CLASSIFICATION"
    NL_GENERATION = "NL_GENERATION"

    def __str__(self) -> str:
        return str(self.value)
