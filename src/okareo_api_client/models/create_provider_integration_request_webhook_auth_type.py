from enum import Enum


class CreateProviderIntegrationRequestWebhookAuthType(str, Enum):
    RETELL_SIGNATURE = "retell_signature"
    TWILIO_SIGNATURE = "twilio_signature"

    def __str__(self) -> str:
        return str(self.value)
