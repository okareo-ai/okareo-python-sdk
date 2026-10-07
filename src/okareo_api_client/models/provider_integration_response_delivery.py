from enum import Enum


class ProviderIntegrationResponseDelivery(str, Enum):
    PULL = "pull"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
