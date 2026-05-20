from enum import Enum


class ProviderIntegrationResponseProvider(str, Enum):
    RETELL = "retell"
    TWILIO = "twilio"

    def __str__(self) -> str:
        return str(self.value)
