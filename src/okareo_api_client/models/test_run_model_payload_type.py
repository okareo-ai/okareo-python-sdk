from enum import Enum


class TestRunModelPayloadType(str, Enum):
    COHERE = "cohere"
    CUSTOM = "custom"
    OPENAI = "openai"
    PINECONE = "pinecone"

    def __str__(self) -> str:
        return str(self.value)
