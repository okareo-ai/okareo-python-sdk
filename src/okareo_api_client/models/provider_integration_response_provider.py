from enum import Enum


class ProviderIntegrationResponseProvider(str, Enum):
    AGENTFORCE = "agentforce"
    LIVEKIT = "livekit"
    RETELL = "retell"
    TWILIO = "twilio"

    def __str__(self) -> str:
        return str(self.value)
