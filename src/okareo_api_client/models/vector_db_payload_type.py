from enum import Enum


class VectorDbPayloadType(str, Enum):
    PINECONE = "pinecone"

    def __str__(self) -> str:
        return str(self.value)
