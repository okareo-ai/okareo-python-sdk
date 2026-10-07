from enum import Enum


class CreateProviderIntegrationRequestWebhookAuthTypeType0(str, Enum):
    LIVEKIT_JWT = "livekit_jwt"
    OAUTH_CLIENT_CREDENTIALS = "oauth_client_credentials"
    RETELL_SIGNATURE = "retell_signature"
    TWILIO_SIGNATURE = "twilio_signature"

    def __str__(self) -> str:
        return str(self.value)
