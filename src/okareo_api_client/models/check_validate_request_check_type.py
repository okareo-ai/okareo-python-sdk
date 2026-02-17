from enum import Enum


class CheckValidateRequestCheckType(str, Enum):
    CODE = "code"
    MODEL = "model"

    def __str__(self) -> str:
        return str(self.value)
