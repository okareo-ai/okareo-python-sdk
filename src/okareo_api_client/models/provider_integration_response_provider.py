from enum import Enum


class ProviderIntegrationResponseProvider(str, Enum):
    RETELL = "retell"
    TWILIO = "twilio"
    VAPI = "vapi"

    def __str__(self) -> str:
        return str(self.value)
