from enum import Enum


class ProviderIntegrationResponseWebhookAuthType(str, Enum):
    RETELL_SIGNATURE = "retell_signature"
    TWILIO_SIGNATURE = "twilio_signature"

    def __str__(self) -> str:
        return str(self.value)
