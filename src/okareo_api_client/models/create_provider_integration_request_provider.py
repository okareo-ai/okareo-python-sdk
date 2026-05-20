from enum import Enum


class CreateProviderIntegrationRequestProvider(str, Enum):
    RETELL = "retell"
    TWILIO = "twilio"

    def __str__(self) -> str:
        return str(self.value)
