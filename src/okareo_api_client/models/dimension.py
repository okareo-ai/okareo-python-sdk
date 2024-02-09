from enum import Enum


class Dimension(str, Enum):
    BREVITY_OUTPUT_ONLY = "brevity_output_only"
    COHERENCE = "coherence"
    COHERENCE_OUTPUT_ONLY = "coherence_output_only"
    CONSISTENCY = "consistency"
    CONSISTENCY_OUTPUT_ONLY = "consistency_output_only"
    FLUENCY = "fluency"
    FLUENCY_OUTPUT_ONLY = "fluency_output_only"
    OVERALL = "overall"
    RELEVANCE = "relevance"
    UNIQUENESS = "uniqueness"

    def __str__(self) -> str:
        return str(self.value)
